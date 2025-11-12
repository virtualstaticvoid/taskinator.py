import logging

import tasktronaut as ttn

logger = logging.getLogger(__name__)


class GreetingProcess(ttn.ProcessDefinition):
    """A simple process that greets the user."""

    def define_process(self, builder: ttn.Builder):
        builder.expected_arguments(name=str)

        builder.task(self.say_hello)
        builder.task(self.say_name)
        builder.task(self.say_goodbye)

    def say_hello(self, name: str):
        logger.info(f"Hello {name}!")

    def say_name(self, name: str):
        logger.info(f"Nice to meet you, {name}.")

    def say_goodbye(self, name: str):
        logger.info(f"Goodbye {name}!")
