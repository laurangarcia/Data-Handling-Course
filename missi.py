import pandas as pd

df = pd.DataFrame(
    {
        'a': list("abcdefghij"),
        'b': range(0, 10)
    }
)

df.iloc[2:5, 0] = None
df.iloc[6:7, 1] = None

df

@pd.api.extensions.register_dataframe_accessor('missing') #Decorador
class MissingMethods:                                     #Clase
    def __init__(self, pandas_obj):
        self._df = pandas_obj

    def number_missing(self):               #Metodo para contar datos faltantes
        return self._df.isna().sum().sum()
    
    def number_complete(self):              #Metodo para contar datos completos
        return self._df.size - self._df.missing.number_missing()
    
    def proportion_missing(self):
        pass

    #probar uso
df = pd.DataFrame(df)

df.missing

df.missing.number_missing()

df.missing.number_complete()
