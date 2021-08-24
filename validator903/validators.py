import pandas as pd
from .types import ErrorDefinition

def validate_103():
    error = ErrorDefinition(
        code='103',
        description='The ethnicity code is either not valid or has not been entered.',
        affected_fields=['ETHNIC'],
    )

    def _validate(dfs):
        if 'Header' not in dfs:
            return {}
        
        header = dfs['Header']
        code_list = [
          'WBRI', 
          'WIRI', 
          'WOTH', 
          'WIRT', 
          'WROM', 
          'MWBC', 
          'MWBA', 
          'MWAS', 
          'MOTH', 
          'AIND', 
          'APKN', 
          'ABAN', 
          'AOTH', 
          'BCRB', 
          'BAFR', 
          'BOTH', 
          'CHNE', 
          'OOTH', 
          'REFU', 
          'NOBT'
        ]

        mask = header['ETHNIC'].isin(code_list)

        validation_error_mask = ~mask
        validation_error_locations = header.index[validation_error_mask]

        return {'Header': validation_error_locations.tolist()}

    return error, _validate

def validate_143():
    error = ErrorDefinition(
        code='143',
        description='The reason for new episode code is not a valid code.',
        affected_fields=['RNE'],
    )

    def _validate(dfs):
        if 'Episodes' not in dfs:
            return {}
        
        episodes = dfs['Episodes']
        code_list = ['S', 'P', 'L', 'T', 'U', 'B']

        mask = episodes['RNE'].isin(code_list) | episodes['RNE'].isna()
        
        validation_error_mask = ~mask
        validation_error_locations = episodes.index[validation_error_mask]

        return {'Episodes': validation_error_locations.tolist()}

    return error, _validate

def validate_144():
    error = ErrorDefinition(
        code='144',
        description='The legal status code is not a valid code.',
        affected_fields=['LS'],
    )

    def _validate(dfs):
        if 'Episodes' not in dfs:
            return {}
        
        episodes = dfs['Episodes']
        code_list = [
          'C1', 
          'C2',
          'D1', 
          'E1', 
          'V2', 
          'V3', 
          'V4', 
          'J1', 
          'J2', 
          'J3', 
          'L1', 
          'L2',
          'L3'
        ]

        mask = episodes['LS'].isin(code_list) | episodes['LS'].isna()
        
        validation_error_mask = ~mask
        validation_error_locations = episodes.index[validation_error_mask]

        return {'Episodes': validation_error_locations.tolist()}

    return error, _validate

def validate_145():
    error = ErrorDefinition(
        code='145',
        description='Category of need code is not a valid code.',
        affected_fields=['CIN'],
    )

    def _validate(dfs):
        if 'Episodes' not in dfs:
            return {}
        
        episodes = dfs['Episodes']
        code_list = [
          'N1', 
          'N2', 
          'N3', 
          'N4', 
          'N5', 
          'N6', 
          'N7', 
          'N8', 
        ]

        mask = episodes['CIN'].isin(code_list) | episodes['CIN'].isna()
        validation_error_mask = ~mask
        validation_error_locations = episodes.index[validation_error_mask]

        return {'Episodes': validation_error_locations.tolist()}

    return error, _validate
 
def validate_146():
    error = ErrorDefinition(
        code='146',
        description='Placement type code is not a valid code.',
        affected_fields=['PLACE'],
    )

    def _validate(dfs):
        if 'Episodes' not in dfs:
            return {}
        
        episodes = dfs['Episodes']
        code_list = [
          'A3', 
          'A4',
          'A5',
          'A6', 
          'H5', 
          'K1', 
          'K2', 
          'P1', 
          'P2', 
          'P3', 
          'R1', 
          'R2', 
          'R3', 
          'R5', 
          'S1', 
          'T0', 
          'T1', 
          'T2', 
          'T3', 
          'T4', 
          'U1', 
          'U2', 
          'U3', 
          'U4', 
          'U5', 
          'U6', 
          'Z1'
        ]

        mask = episodes['PLACE'].isin(code_list) | episodes['PLACE'].isna()
        
        validation_error_mask = ~mask
        validation_error_locations = episodes.index[validation_error_mask]

        return {'Episodes': validation_error_locations.tolist()}

    return error, _validate

def validate_149():
    error = ErrorDefinition(
        code='149',
        description='Reason episode ceased code is not valid. ',
        affected_fields=['REC'],
    )

    def _validate(dfs):
        if 'Episodes' not in dfs:
            return {}
        
        episodes = dfs['Episodes']
        code_list = [
          'E11',
          'E12', 
          'E2', 
          'E3', 
          'E4A', 
          'E4B', 
          'E13', 
          'E41',
          'E45', 
          'E46', 
          'E47', 
          'E48', 
          'E5', 
          'E6', 
          'E7', 
          'E8',
          'E9',
          'E14', 
          'E15',
          'E16', 
          'E17', 
          'X1'
        ]

        mask = episodes['REC'].isin(code_list) | episodes['REC'].isna()
        
        validation_error_mask = ~mask
        validation_error_locations = episodes.index[validation_error_mask]

        return {'Episodes': validation_error_locations.tolist()}

    return error, _validate

def validate_167():
    error = ErrorDefinition(
        code='167',
        description='Data entry for participation is invalid or blank.',
        affected_fields=['REVIEW_CODE'],
    )

    def _validate(dfs):
        if 'Reviews' not in dfs:
            return {}
        
        review = dfs['Reviews']
        code_list = ['PN0', 'PN1', 'PN2', 'PN3', 'PN4', 'PN5', 'PN6', 'PN7']

        mask = review['REVIEW'].notna() & review['REVIEW_CODE'].isin(code_list) | review['REVIEW'].isna() & review['REVIEW_CODE'].isna()

        validation_error_mask = ~mask
        validation_error_locations = review.index[validation_error_mask]

        return {'Reviews': validation_error_locations.tolist()}
      
    return error, _validate 

def validate_101():
    error = ErrorDefinition(
        code='101',
        description='Gender code is not valid.',
        affected_fields=['SEX'],
    )

    def _validate(dfs):
        if 'Header' not in dfs:
            return {}
        
        header = dfs['Header']
        code_list = [1, 2]

        mask = header['SEX'].isin(code_list)

        validation_error_mask = ~mask
        validation_error_locations = header.index[validation_error_mask]

        return {'Header': validation_error_locations.tolist()}
      
    return error, _validate 

def validate_141():
    error = ErrorDefinition(
        code = '141',
        description = 'Date episode began is not a valid date.',
        affected_fields=['DECOM'],
    )

    def _validate(dfs):
        if 'Episodes' not in dfs:
            return {}
        else:
            episodes = dfs['Episodes']
            mask = pd.to_datetime(episodes['DECOM'], format='%d/%m/%Y', errors='coerce').notna()

            na_location = episodes['DECOM'].isna()

            validation_error_mask = ~mask & ~na_location
            validation_error_locations = episodes.index[validation_error_mask]

            return {'Episodes': validation_error_locations.tolist()}
    
    return error, _validate

def validate_102():
    error = ErrorDefinition(
        code='102',
        description='Date of birth is not a valid date.',
        affected_fields=['DOB'],
    )

    def _validate(dfs):
        if 'Header' not in dfs:
            return {}
        else:
            header = dfs['Header']
            mask = pd.to_datetime(header['DOB'], format='%d/%m/%Y', errors='coerce').notna()

            validation_error_mask = ~mask
            validation_error_locations = header.index[validation_error_mask]

            return {'Header': validation_error_locations.tolist()}
    
    return error, _validate

def validate_392c():
    error = ErrorDefinition(
        code='392c',
        description='Postcode(s) provided are invalid.',
        affected_fields=['HOME_POST', 'PL_POST'],
    )

    def _validate(dfs):
        if 'Episodes' not in dfs or 'postcodes' not in dfs['metadata']:
            return {}
        else:
            episodes = dfs['Episodes']
            postcode_list = set(dfs['metadata']['postcodes']['pcd'].str.replace(' ', ''))

            is_valid = lambda x: str(x).replace(' ', '') in postcode_list
            home_provided = episodes['HOME_POST'].notna()
            home_valid = episodes['HOME_POST'].apply(is_valid)
            pl_provided = episodes['PL_POST'].notna()
            pl_valid = episodes['PL_POST'].apply(is_valid)

            error_mask = (home_provided & ~home_valid) | (pl_provided & ~pl_valid)

            return {'Episodes': episodes.index[error_mask].tolist()}

    return error, _validate

def validate_213():
    error = ErrorDefinition(
        code='213',
        description='Placement provider information not required.',
        affected_fields=['PLACE_PROVIDER'],
    )

    def _validate(dfs):
        if 'Episode' not in dfs:
            return {}
        else:
            df = dfs['Episode']
            mask = df['PLACE'].isin(['T0','T1','T2','T3','T4','Z1']) & df['PLACE_PROVIDER'].notna()
            return {'Episode': df.index[mask].tolist()}
    
    return error, _validate

def validate_168():
    error = ErrorDefinition(
        code='168',
        description='Unique Pupil Number (UPN) is not valid. If unknown, default codes should be UN1, UN2, UN3, UN4 or UN5.',
        affected_fields=['UPN'],
    )

    def _validate(dfs):
        if 'Header' not in dfs:
            return {}
        else:
            df = dfs['Header']
            mask = df['UPN'].str.fullmatch(r'(^((?![IOS])[A-Z]){1}(\d{12}|\d{11}[A-Z]{1})$)|^(UN[1-5])$',na=False)
            mask = ~mask
            return {'Header': df.index[mask].tolist()}
    
    return error, _validate
