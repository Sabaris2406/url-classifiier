import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

class   NIDSFeaturePreprocessor:
    def __init__(self):
        # The UNSW-NB15 dataset has these three main categorical columns
        self.categorical_cols = ['proto', 'service', 'state']
        # handle_unknown ensures that if a new protocol appears in production, it doesn't crash
        self.encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)

    def fit(self, df):
        """Fits the encoder on the training data."""
        self.encoder.fit(df[self.categorical_cols])

    def transform(self, df):
        """Transforms raw network flow data into a numeric feature matrix."""
        df_processed = df.copy()
        
        # Drop columns that shouldn't be used for prediction
        # 'id' is just an index, 'attack_cat' is the multiclass label, 'label' is the binary target
        cols_to_drop = ['id', 'attack_cat', 'label']
        df_processed = df_processed.drop(columns=[c for c in cols_to_drop if c in df_processed.columns], errors='ignore')

        # Encode categorical columns
        df_processed[self.categorical_cols] = self.encoder.transform(df_processed[self.categorical_cols])
        
        # Ensure all data is numeric (XGBoost requires numeric inputs)
        df_processed = df_processed.apply(pd.to_numeric, errors='coerce').fillna(0)
        
        return df_processed