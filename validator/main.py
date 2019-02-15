from pandas import DataFrame, read_csv
import pandas as pd


def read_file_panda():
    file = r'email.csv'
    df = pd.read_csv(file)

    # Filtering columns by NULL, we need only those not processed
    df_mod = df[df['SYNTAX'].isnull() | df['MX_RECORD'].isnull() | df['SMTP_HELLO'].isnull()]

    for data in df_mod['EMAIL']:
        print(data)


if __name__ == '__main__':
    read_file_panda()

