import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def build_feature_pipeline(X_train):
    """Crea el pipeline de preprocesamiento de características"""
    num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = X_train.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ])
    
    return preprocessor

def prepare_data(filepath, target_col='Pago_atiempo'):
    """Carga el dataset, elimina leakage y retorna los conjuntos train/test"""
    df = pd.read_excel(filepath)
    X = df.drop(columns=[target_col, 'fecha_prestamo', 'puntaje'])
    y = df[target_col]
    
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    cat_cols = X_tr.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    X_tr[cat_cols] = X_tr[cat_cols].astype(str)
    X_te[cat_cols] = X_te[cat_cols].astype(str)
    
    return X_tr, X_te, y_tr, y_te
