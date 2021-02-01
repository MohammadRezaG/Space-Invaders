from pygame.image import load
import configparser
import os


class Setings():
    @staticmethod
    def load_setings(path: str = 'setings.INI'):
        if os.path.isfile(path):
            return Setings._load(path)
        else:
            Setings._create_default_setting(path)
            return Setings._load(path)

    @staticmethod
    def default(path: str = 'setings.INI'):
        """
        set setting to default
        """
        Setings._delete_setings(path)
        Setings._create_default_setting(path)

    def _delete_setings(path):
        """
        delete setings setings.INI
        """
        os.remove(path)

    def _create_default_setting(path):
        """
        create default setting setings.INI
        """
        try:
            from configparser import ConfigParser
        except ImportError:
            from ConfigParser import ConfigParser  # ver. < 3.0

        # instantiate
        config = ConfigParser()

        # update existing value
        config['Assets Paths'] = {
            'background': 'assets\\images\\background.png',
            'bullet': 'assets\\images\\bullet.png',
            'bullet_red': 'assets\\images\\bullet_red.png',
            'icon' : 'assets\\images\\RedInvader.png',

            'ship': 'assets\\images\\Ship.png',
            'ship_cr': 'assets\\images\\ShipCrushedRight.png',
            'ship_cl': 'assets\\images\\ShipCrushedLeft.png',
            'ship_cc': 'assets\\images\\ShipWhite.png',

            'invadera1': 'assets\\images\\InvaderA1.png',
            'invadera2': 'assets\\images\\InvaderA2.png',
            'invaderb1': 'assets\\images\\InvaderB1.png',
            'invaderb2': 'assets\\images\\InvaderB2.png',
            'invaderc1': 'assets\\images\\InvaderC1.png',
            'invaderc2': 'assets\\images\\InvaderC2.png',

        }
        config['castle'] = {
            'castle_location': [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 0, 0, 1],
            ],
            'start_x': 50,
            'start_y': 500,
            'column': 5,
            'row': 5,
            'block_l3': (9, 255, 14),
            'block_l2': (27, 255, 30),
            'block_l1': (114, 255, 133),
        }
        config['alien'] = {
            'margin_width': 200,
            'margin_height': 20,
            'column': 'd',
            'Row': 5,
            'width_x': 10,
            'width_y': 10,
            'movement': 10,
            'alien_column_config': r'{"0":{"path1":"InvaderA1","path2":"InvaderA2"},"1":{"path1":"InvaderB1","path2":"InvaderB2"},"2":{"path1":"InvaderB1","path2":"InvaderB2"},"3":{"path1":"InvaderC1","path2":"InvaderC2"},"4":{"path1":"InvaderC1","path2":"InvaderC2"}}'
        }
        config['player 1'] = {
            'margin': 20,
            'speed': 3
        }

        with open(path, 'w') as configfile:
            config.write(configfile)

    def _load(path):
        setings = {}
        try:
            from configparser import ConfigParser
        except ImportError:
            from ConfigParser import ConfigParser  # ver. < 3.0

        # instantiate
        config = ConfigParser()

        # parse existing file
        try:
            config.read(path)
        except Exception as e:
            print(e)

        for section in config.sections():
            setings[section] = {}
            for key, val in config.items(section):
                setings[section][key] = val
        return setings


class Assets ():

    def __init__(self, setings: Setings):
        if not self.load_assets(setings['Assets Paths']):
            Setings.default()

    def load_assets(self, paths):
        """
        load_assets 
        failed retern 0 
        sucsses retern 1
        """
        try:
            self.background = load(paths['background'])
            self.bullet = load(paths['bullet'])
            self.bullet_red = load(paths['bullet_red'])
            self.icon = load(paths['icon'])

            self.Ship = load(paths['ship'])
            self.Ship_CR = load(paths['ship_cr'])
            self.Ship_CL = load(paths['ship_cl'])
            self.Ship_CC = load(paths['ship_cc'])

            self.InvaderA1 = load(paths['invadera1'])
            self.InvaderA2 = load(paths['invadera2'])
            self.InvaderB1 = load(paths['invaderb1'])
            self.InvaderB2 = load(paths['invaderb2'])
            self.InvaderC1 = load(paths['invaderc1'])
            self.InvaderC2 = load(paths['invaderc2'])

        except Exception as e:
            print(" "+str(e))
            return 0
        else:
            return 1

    def load_sond(parameter_list):
        """
        load_sond
        failed retern 0 
        sucsses retern 1
        """
        pass
