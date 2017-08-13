from faker import Factory
from random import uniform, choice, random
from decimal import Decimal
import pandas as pd
import string

DIG_LIST = list(range(10))
LET_LIST = list(string.ascii_uppercase)

FAKE = Factory.create('en_CA')


class FakeData:
    """
    Generate fake data with formatting noise.

    This class initializes a dictionary that will hold data tailored for the
    Canadian province of British Columbia. Boolean values specified when the
    class instance is initialized will determine how the data is split between
    different dictionary keys.

    Attributes:
        data_dict (dict): The structure that contains the fake data.
        fake_factory (class instance): Instance of faker package to generate names and jobs
        street_list (list): List of streets in Vancouver and N. Vancouver to sample from.
        city_list (list): List of cities in BC to sample from.
        split_name (bool): True will split first and last names into different dict keys
        split_addr (bool): Ture will split address into address1, address2, city, province, postal keys
    """

    def __init__(self,
                 split_name=True,
                 split_addr=False):

        self.data_dict = {}  # Initialize the structure that will hold all the fake data.

        with open('street_names.csv', 'r') as file:
            self.street_list = [line.rstrip('\n') for line in file]

        with open('city_names.csv', 'r') as file:
            self.city_list = [line.rstrip('\n') for line in file]

        self.split_name = split_name
        self.split_addr = split_addr

    def check_key(self, key, data_out):
        """
        Adds data to key in data_dict.

        Checks whether data_dict contains key. If it does, adds data_out to the
        corresponding list. If it doesn't, initializes the list under key with data_out.
        :param key: The dictionary key that corresponds to field of data.
        :type key: string
        :param data_out: The data to be included in the list under data_dict[key]
        :type data_out: string
        :return: returns self with data_out added to key in data_dict
        """
        if key in self.data_dict:
            self.data_dict[key].append(data_out)
        elif key not in self.data_dict:
            self.data_dict[key] = [data_out]

    def generate_sin(self):
        """
        Generates a valid Canadian SIN. Introduces formatting noise.

        :return: self. Adds a new SIN to the list under self.data_dict["sin"]
        """
        first_dig = DIG_LIST[1:8] + [DIG_LIST[-1]]  # first digit of strings is 1-7 or 9
        sin_list = [choice(first_dig)] + [choice(DIG_LIST) for _ in range(7)]  # randomly select the next 7 nums
        chk = [1, 2, 1, 2, 1, 2, 1, 2]
        check = sum(map(lambda x: (x-9) if (x > 9) else x,
                        [dig * chk for dig, chk in zip(sin_list, chk)]))  # Luhn alg on first 8 digits
        sin_list += list(filter(lambda x: (x + check) % 10 == 0,
                                DIG_LIST))  # select the necessary digit to satisfy Luhn algorithm

        sin_noise = random()

        if sin_noise < 0.33:  # insert spaces to format XXX XXX XXX
            sin_list = sin_list[:3] + [" "] + sin_list[3:6] + [" "] + sin_list[6:]
        elif sin_noise > 0.66:  # insert spaces to format XXX-XXX-XXX
            sin_list = sin_list[:3] + ["-"] + sin_list[3:6] + ["-"] + sin_list[6:]

        sin_out = "".join([str(i) for i in sin_list])  # join digits in valid SIN list
        self.check_key(key="sin", data_out=sin_out)  # check key in data_dict and add sin_out

    def generate_address(self):
        """
        Generates a BC address with formatting noise.

        :return: self with address keys added to data_dict
        """

        def _generate_address1():
            """Generates a street number and name."""
            st_no = str(round(uniform(1, 20000)))
            street = choice(self.street_list)  # Samples from list of streets
            return st_no + " " + street

        def _generate_address2(unit_type):
            """Generates an apartment number."""
            apt_no = str(round(uniform(1, 16))) + str(round(uniform(1, 20)))
            if unit_type:
                apt = choice(['Apt ', 'apt ', 'Unit ', 'unit ', 'suite ', 'Suite '])
                return apt + apt_no  # Format: A(a)pt/U(u)nit/S(s)uite XXXX
            else:
                return apt_no + "-"  # Format XXXX-(_generate_address1)

        def _generate_city():
            """Sample from list of BC cities"""
            return choice(self.city_list)

        def _generate_postal():
            """Generates BC postal code with formatting noise."""
            postal_1 = 'V' + str(choice(DIG_LIST)) + choice(LET_LIST)  # First 3 vals
            postal_2 = str(choice(DIG_LIST)) + choice(LET_LIST) + str(choice(DIG_LIST))  # Last 3 vals
            if random() > 0.5:
                joiner = ""  # Format V1V1V1
            else:
                joiner = " "  # Format V1V 1V1
            return joiner.join([postal_1, postal_2])

        def _const_addr1(format):
            """Generates addresses such that 85% have no apt or have the apt out in front."""
            if 0.125 < format < 0.25:  # Format: Apt XXX, XXX Street
                addr1 = _generate_address2(unit_type=True) + choice([" ", ", "]) + _generate_address1()
                return addr1
            elif 0.25 < format < 0.5:  # Format: XXX-XXX Street
                return _generate_address2(unit_type=False) + _generate_address1()
            elif format > 0.5:  # Format: XXX Street
                return _generate_address1()

        address_noise = random()

        if self.split_addr:  # Split address values into separate columns: address1, address2, city, province, postal
            if address_noise < 0.125:  # Format: address1: XXX Street; address2: Apt XXX
                addr1_out = _generate_address1()
                addr2_out = _generate_address2(unit_type=True)
            else:  # Format: address1: _const_addr1; address2: blank
                addr1_out = _const_addr1(address_noise)
                addr2_out = ""

            city_out = _generate_city()
            prov_out = "BC"
            postal_out = _generate_postal()

            # Check data_dict for address1, address2, city, province, postal keys and add values
            self.check_key(key="address1", data_out=addr1_out)
            self.check_key(key="address2", data_out=addr2_out)
            self.check_key(key="city", data_out=city_out)
            self.check_key(key="province", data_out=prov_out)
            self.check_key(key="postal", data_out=postal_out)

        else:  # All address values are in the same line
            if address_noise < 0.125:  # Format: XXX Street, Apt XXX, city, prov, postal
                addr1_2 = _generate_address1() + choice([" ", ", "]) + _generate_address2(unit_type=True)
            else:  # Format: _const_addr1, city, prov, postal
                addr1_2 = _const_addr1(address_noise)

            address_elms = [addr1_2, _generate_city(), "BC " + _generate_postal()]
            address_out = ", ".join(address_elms)  # Join all of the address components together

            self.check_key(key="address", data_out=address_out)  # Check data_dict for address key and add value

    def generate_name(self):
        """
        Generates a first and last name using the faker package.

        :return: self with values added name keys in data_dict.
        """
        first_name_out = FAKE.first_name()
        last_name_out = FAKE.last_name()
        if self.split_name:  # Split name into first and last columns
            self.check_key("first_name", first_name_out)
            self.check_key("last_name", last_name_out)
        else:  # Format: last name, first name
            last_first_out = last_name_out + choice([", ", ","]) + first_name_out
            self.check_key("name", last_first_out)

    def generate_wage(self):
        """
        Generates a monetary value (e.g. XXXX.XX) between 50.00 and 7000.00

        :return: self with a monetary value added to the wage key in data_dict
        """
        wage_out = str(Decimal(uniform(50, 7000)).quantize(Decimal('.01')))
        self.check_key("wage", wage_out)

    def generate_job(self):
        """
        Generates a job title using faker.

        :return: self with a job title added to the job key in data_dict
        """
        job_out = FAKE.job()
        self.check_key("job", job_out)
        # return self

    def generate_sheet(self, num_records,
                       name=True,
                       sin=True,
                       address=True,
                       wage=True,
                       job=False):
        """
        Adds a specified number of records to data_dict.

        :param num_records: Number of records to generate in data_dict
        :type num_records: int
        :param name: True to generate num_records names
        :param sin: True to generate num_records SINs
        :param address: True to generate num_records addresses
        :param wage: True to generate num_records wage values
        :param job: True to generate num_records job types

        :return: self with num_records entries in each of the fields specified as True
        """
        if name:
            for _ in range(num_records):
                self.generate_name()

        if sin:
            for _ in range(num_records):
                self.generate_sin()

        if address:
            for _ in range(num_records):
                self.generate_address()

        if wage:
            for _ in range(num_records):
                self.generate_wage()

        if job:
            for _ in range(num_records):
                self.generate_job()

        return self

    def to_dataframe(self):
        """
        Generates a DataFrame from data_dict

        :return: DataFrame with a column for each key in data_dict
        :rtype: Pandas DataFrame
        """
        df_out = pd.DataFrame.from_dict(self.data_dict)
        return df_out

# Uncomment to test Data class

# data_test = FakeData(split_name=False, split_addr=True)
# data_test.generate_wage()
# data_test.generate_address()
# data_test.generate_sin()
# data_test.generate_name()
# data_test.generate_job()
# print(data_test.data_dict)
# data_test.generate_sheet(job=True, num_records=2000)
# data_test_df = data_test.to_dataframe()
# print(data_test_df.head(5))





