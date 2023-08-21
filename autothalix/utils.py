import csv
from autothalix.logging import logger
from thales_remote.connection import ThalesRemoteConnection
from thales_remote.script_wrapper import ThalesRemoteScriptWrapper


def initialize_experiment():
    """
    Initialize the experiment by connecting to the Thales Zennium and calibrating the offsets
    :return: zennium_connection, zahner_zennium
    :rtype: ThalesRemoteConnection, ThalesRemoteScriptWrapper
    """
    zennium_connection = ThalesRemoteConnection()
    zennium_connection.connectToTerm("localhost", "ScriptRemote")  # do not change to anything besides localhost
    zahner_zennium = ThalesRemoteScriptWrapper(zennium_connection)
    zahner_zennium.forceThalesIntoRemoteScript()
    zahner_zennium.calibrateOffsets()
    return zennium_connection, zahner_zennium


def write_dict_to_csv(dict_data, file_path):
    """
    Write a dictionary to a csv file with the keys as the header row and the values as the data rows
    :param dict_data:
    :param file_path:
    :return:
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(dict_data.keys())

        # Write the data rows
        for row in zip(*dict_data.values()):
            writer.writerow(row)


def safe_pot(func):
    def wrapper(self, *args, **kwargs):
        logger.info('Manually enabling potentiostat')
        self.wr_connection.enablePotentiostat()
        try:
            result = func(self, *args, **kwargs)
        except Exception as e:  # disables potentiostat if an error occurs
            self.wr_connection.disablePotentiostat()
            logger.error(f'Error occurred during {str(self)} measurements: "{e}"')
            logger.info("Potentiostat disabled")
            raise e
        self.wr_connection.disablePotentiostat()
        logger.info("Potentiostat disabled")
        return result

    return wrapper
