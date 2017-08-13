fakeBC is a module that generates fake data specific for the Canadian province of British Columbia.

At this point, the module can generate fake data for 5 different fields: names, addresses, Canadian SINs, wages, and job titles. Names and job titles are generated using the faker Python package (https://pypi.python.org/pypi/Faker). 

Details on each field:
- Names: First and last names generated using faker. If split_name is selected, generates separate fields for first and last name, otherwise formats them last name, first name.

- Addresses: Generates values for address 1, address 2, city, province, and postal code.

- SINs: Distributed uniformly across provinces (i.e. the first digit is sampled from a uniform distribution). Generated to satisfy the Luhn algorithm.

- Wage: Monetary value of the form XXXX.XX sampled from a uniform distribution from [50.00, 7000.00]. The limits on this value were selected to correspond to a monthly paycheque. 

- Job title: Job titles generated using faker.

Use example

```
import fakeBC
test_data = fakeBC.FakeData(split_name=False, split_addr=True)
data_test.generate_wage()
data_test.generate_address()
data_test.generate_sin()
data_test.generate_name()
data_test.generate_job()
print(data_test.data_dict)

out:

{'province': ['BC'], 'postal': ['V2R 7U8'], 'sin': ['775 938 939'], 'city': ['Grand Forks'], 'address1': ['5424 Leovista Avenue'], 'name': ['Ballard,Bradley'], 'address2': ['Suite 1217'], 'wage': ['3547.30'], 'job': ['Leisure centre manager']}

data_test.generate_sheet(num_records=50, job=True)
data_test_df = data_test.to_dataframe()
print(data_test_df.head(5))

out:

			       address1  address2          city  
0                 12896 West 2nd Street  unit 139      Granisle   
1                      7174 Clegg Place             Port Edward   
2                  19230 Beaufort Place              Chilliwack   
3         1218-16053 Sleil-waututh Road            Mission City   
4  134-13244 Mt Seymour Offramp Parkway              Chilliwack   

                                    job              name   postal province  
0      Accountant, chartered management     Morris,Justin   V4Y6C4       BC   
1                  Optician, dispensing    Navarro,Connie   V2H7M8       BC   
2  English as a second language teacher  Elliott, William  V7R 8Y6       BC   
3               Secretary/administrator   Marshall,Steven  V1P 1N0       BC   
4                            Translator       Wilson,Tony   V0L1V4       BC   

           sin     wage  
0  192-617-553  3932.84  
1  507-211-662   677.62  
2  769 368 051  1631.23  
3    601280746  5814.72  
4  630 927 630  5519.77  
```

Packages used:
Faker 0.7.12 https://pypi.python.org/pypi/Faker
Pandas 0.18.1 http://pandas.pydata.org
