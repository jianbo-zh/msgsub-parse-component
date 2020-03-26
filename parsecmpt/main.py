#!/usr/bin/env python

import click
import json
from kafka import KafkaConsumer
from kafka import KafkaProducer

from . import helperz
from . import constz
from .loggerz import logger
from .dealer.html import handler as htmlhandler
from .dealer.xml import handler as xmlhandler
from .dealer.json import handler as jsonhandler
import threadpool

@click.command()
@click.option(
    "--broker-list",
    type=str,
    default="localhost:9092",
    help="all brokens",
    show_default=True,
    show_envvar=True,
    envvar="KAFKA_BROKER_LIST",
    metavar="brokerList",
)
@click.option(
    "--from-topic",
    type=str,
    required=True,
    default="crawler_task",
    help="subscribe topic",
    prompt="Please enter subscribe topic",
    metavar="fromTopic",
)
@click.option(
    "--to-topic",
    type=str,
    required=True,
    default="deal_task",
    help="publish topic",
    prompt="Please enter publish topic",
    metavar="toTopic",
)
@click.option(
    "--group-id", default=None, type=str, help="consumer group id", metavar="groupId",
)
@click.option(
    "--thread-count",
    default=3,
    type=click.IntRange(1, 10, clamp=True),
    help="run thread count",
    metavar="threadCount",
)
@click.option(
    "--level",
    type=click.IntRange(1, 5, clamp=True),
    default=1,
    show_default=True,
    help="log level [1-5]",
    metavar="logLevel",
)
def datadeal(broker_list, from_topic, to_topic, group_id, thread_count, level):
    try:
        logger.setLevel((6 - level) * 10)

        tpool = threadpool.threadPoolManager(thread_count, 10)

        brokers = list(map(lambda s: str.strip(s), broker_list.split(",")))

        # 消费者
        consumer = KafkaConsumer(
            from_topic, group_id=group_id, bootstrap_servers=brokers,
        )

        # 生产者
        producer = KafkaProducer(bootstrap_servers=brokers)

        # 消息处理逻辑
        def msg_deal(datas):
            for data in datas:
                producer.send(to_topic, value=bytes(json.dumps(data), encoding='utf-8'))

        # 事件循环
        for msg in consumer:
            logger.debug(
                "%s:%s:%s key=%s value=%s"
                % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
            )

            # 消息数据
            try:
                msg_data = json.loads(msg.value)
                
            except json.JSONDecodeError as e:
                logger.warning("msg.value[%s] can not decode", msg.value)
                continue

            try:
                type_data = msg_data["content_type"] if "content_type" in msg_data else None
                content_type = helperz.get_content_type(type_data)

            except ValueError as e:
                logger.warning(e)
                continue

            content = msg_data["content"] if "content" in msg_data else ''
            tasks = msg_data["tasks"] if "tasks" in msg_data else []

            try:
                if content_type == constz.CT_HTML:
                    datas = htmlhandler(content, tasks)
                elif content_type == constz.CT_XML:
                    datas = htmlhandler(content, tasks)
                elif content_type == constz.CT_JSON:
                    datas = htmlhandler(content, tasks)
                else:
                    # nothing
                    pass
            except Exception as e:
                logger.error(e)
                continue
            else:
                tpool.add_work(msg_deal, datas)


    except Exception as e:
        logger.error(e)
    
    finally:
        tpool.close_thread_pool()
    


if __name__ == "__main__":
    datadeal()
