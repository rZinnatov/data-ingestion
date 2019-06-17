from extract import Extractor


def performEtl(config):
    etlConfig = EtlConfig(config)
    Extractor(etlConfig).run()


class EtlConfig:
    def __init__(self, config):
        self.id = config['id']
        self.number_of_instances = config['number_of_instances']
        self.transform = config['transform']
        self.load = config['load']

        self.extractConfig = ExtractConfig(config)
        self.transformConfig = TransformConfig(config)
        self.loadConfig = LoadConfig(config)


class ExtractConfig:
    def __init__(self, config):
        self.id = config['id']
        self.number_of_instances = config['number_of_instances']
        self.url = config['extractUrl']


class TransformConfig:
    def __init__(self, config):
        self.id = config['id']
        self.number_of_instances = config['number_of_instances']
        self.types = config['types']
        self.handler = config['transformHandler']


class LoadConfig:
    def __init__(self, config):
        self.id = config['id']
        self.number_of_instances = config['number_of_instances']
        self.connectionString = config['connectionString']
