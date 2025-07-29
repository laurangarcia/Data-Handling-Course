# %% [markdown]
# ## Importar librerías

# %%
import janitor
import nhanes.load
import numpy as np
import pandas as pd
import missingno

# %% [markdown]
# ## Importar funciones personalizadas

# %%
import pandas_missing_extension  # si el archivo se llama pandas_missing_extension.py


# %% [markdown]
# ## Cargar los datos de NHANES

# %%
nhanes_raw_df= (
    nhanes.load.load_NHANES_data(year="2017-2018")
    .clean_names(case_type = "snake")
)

nhanes_raw_df.shape

# %% [markdown]
# ## Procesar los datos de NHANES

# %%
import numpy as np

nhanes_df = (
    nhanes_raw_df
    .select_columns(
        "general_health_condition",
        "age_in_years_at_screening",
        "gender",
        "current_selfreported_height_inches",
        "current_selfreported_weight_pounds",
        "doctor_told_you_have_diabetes",
        "60_sec_pulse30_sec_pulse2",
        "total_cholesterol_mgdl"
    )
    .rename_columns({
        "age_in_years_at_screening": "age",
        "current_selfreported_height_inches": "height",
        "current_selfreported_weight_pounds": "peso",
        "doctor_told_you_have_diabetes": "diabetes",
        "60_sec_pulse30_sec_pulse2": "pulso",
        "total_cholesterol_mgdl": "total_cholesterol"
    })
    .replace({
        "height": {9999: np.nan, 7777: np.nan},
        "peso": {9999: np.nan, 7777: np.nan},
        "diabetes": {"Borderline": np.nan}
    })
    .missing.sort_variables_by_missingness()
    .dropna(
        subset = ["diabetes"],
        how = "any"
    )
    .transform_column(
        column_name = "diabetes",
        function = lambda s: s.astype(int),
        elementwise = False
    )
)


# %% [markdown]
# ## Visualizar los valores faltantes

# %%
(
    nhanes_df
    .missing.sort_variables_by_missingness()
    .pipe(missingno.matrix, sort = "descending")
)


# %% [markdown]
# Analizando el gráfico, nos damos cuenta que hay variables que no tienen valores faltantes, osea que hay valores qu aparecen conjuntamente y son faltantes

# %%
(
    nhanes_df
    .missing.sort_variables_by_missingness()
    .missing.missing_upsetplot()
)

# %% [markdown]
# Reviando la relación de los valores faltantes, podriamos imputarlo o eliminarlo

# %%
nhanes_df

# %%
# Aplica dropna pero sin sobrescribir con Axes
nhanes_df = (
    nhanes_df
    .dropna(  # Eliminamos las filas que tengan TODOS esos datos faltantes en las columnas
        subset=["pulso", "total_cholesterol", "general_health_condition", "peso", "height"], 
        how="all"
    )
)

# Aplica el método personalizado .missing
nhanes_df = nhanes_df.missing.sort_variables_by_missingness()

# Luego visualiza, pero sin sobrescribir nhanes_df
missingno.matrix(nhanes_df, sort="descending")


# %% [markdown]
# ## Eliminar valores faltantes

# %%
nhanes_df.shape

# %%



