#This will produce the patient journey timelines for medicine administration.

import os 
import pandas as pd 
import numpy as np 
import json 
import chardet



class TimelineGenerator:
    def __init__(self, config_path):
        # Read the configuration from the JSON file
        with open(config_path, 'r') as json_file:
            config = json.load(json_file)
        
        # Store the configuration values as class attributes
        self.data_path = config['Paths']['data_path']
        # self.log_path = config['Paths']['log_path']


#loading functions
    def load_med(self):
   # Load configuration from config.json
        with open('medtimeline/config.json', 'r') as json_file:
            config = json.load(json_file)

        # Construct the full path to the 'Data' folder and 'csv_file_name'
        medications_csv_path = config['Paths']['medications_csv_path']

        # Load the CSV file
        med = pd.read_csv(medications_csv_path)

        # Rename columns
        med = med.rename(columns={
            'drug_code': 'code',
            'start_datetime': 'start_date',
            'end_datetime': 'end_date_meds',
            'MedicationOrderKey': 'medication_order_key'
        })

        med=med.drop_duplicates()
        return med
    
    def load_surgery(self):
    # Load configuration from config.json
        with open('medtimeline/config.json', 'r') as json_file:
            config = json.load(json_file)

        # Construct the full path to the 'Data' folder and 'csv_file_name'
        surgery_csv_path = config['Paths']['surgery_csv_path']

        # Load the CSV file
        surgery = pd.read_csv(surgery_csv_path)

        surgery = surgery.rename(columns={
            'start_datetime':'start_date',
            'end_datetime':'end_date_surg',
            'opert_name':'operation_urgency',
            'spect_name':'operation_name',
            'cancelled_datetime':'cancelled_date',
            'procedure_code':'code'
        })
        
        surgery=surgery.drop_duplicates()
        return surgery
    
    def load_diagnoses(self):
        # Load configuration from config.json
        with open('medtimeline/config.json', 'r') as json_file:
            config = json.load(json_file)

        # Construct the full path to the 'Data' folder and 'dummy_data_diagnosis.csv'
        diagnosis_csv_path = config['Paths']['diagnosis_csv_path']

        # Load the CSV file
        diagnoses = pd.read_csv(diagnosis_csv_path)

        diagnoses=diagnoses.rename(columns={
            'diag_local_code':'code',
            'start_datetime':'start_date',
            'end_datetime':'end_date_diag',
            'epic_diagnosis_source_name':'diagnosis_source',
            'diag_name':'diagnosis'
            })
        
        diagnoses=diagnoses.drop(['diag_nat_code','diag_supl_name','diag_supl_local_code','epic_diagnosis_source_code'], axis=1)
                                 
        categories = {
            'Cardiovascular Disorders': [
                'Adjustment and management of cardiac devices',
                'Adjustment and management of vascular access device',
                'Atrial septal defect',
                'Atrioventricular septal defect',
                'Coarctation of aorta',
                'Congenital insufficiency of aortic valve',
                'Congenital malformation of heart, unspecified',
                'Congenital pulmonary valve stenosis',
                'Congenital stenosis of aortic valve',
                'Congenital tricuspid stenosis',
                'Ebstein anomaly',
                'Heart transplant failure and rejection',
                'Heart transplant status',
                'Hypoplastic left heart syndrome',
                'Malformation of coronary vessels',
                'Other cardiomyopathies',
                'Other congenital malformations of aorta',
                'Other congenital malformations of great veins',
                'Other congenital malformations of pulmonary artery',
                'Other specified cardiac arrhythmias',
                'Other specified complications of cardiac and vascular prosthetic devices, implants and grafts',
                'Other specified conduction disorders',
                'Other specified congenital malformation syndromes NEC',
                'Other specified congenital malformations of heart',
                'Other specified diseases of pulmonary vessels',
                'Primary pulmonary hypertension',
                'Stenosis of pulmonary artery',
                'Tetralogy of Fallot',
                'Thoracic aortic aneurysm, without mention of rupture',
                'Ventricular premature depolarization',
                'Ventricular septal defect',
                'Ventricular tachycardia'
            ],
            'Dental and Hearing': [
                'Dental caries, unspecified',
                'Examination of ears and hearing'
            ], 
                'Pain and Symptoms': [
                'Acute pain',
                'Chest pain, unspecified',
                'Palpitations',
                'Syncope and collapse',
            ],
            'Developmental Disorders': [
                'Down syndrome, unspecified',
                'Marfan syndrome',
            ],
            'Hypertension': [
                'Essential (primary) hypertension',
            ],
            'Nutrition and Feeding': [
                'Feeding difficulties and mismanagement',
            ],
            'Respiratory Disorders': [
                'Other disorders of lung',
                'Other specified diseases of upper respiratory tract',
            ],
            'Electrocardiograms and Examinations': [
                'Examination of ears and hearing',
                'Laboratory examination',
                'Special screening examination for cardiovascular disorders',
            ],
            'Surgical Procedures and Complications': [
                'Follow-up examination after surgery for other conditions',
                'Mech compl of other cardiac & vascular devices and implants',
                'Other specified postsurgical states',
                'Presence of electronic cardiac devices',
                'Presence of other cardiac and vascular implants and grafts',
                'Presence of other heart-valve replacement',
            ],
            'Miscellaneous': [
                'Other ill-defined heart diseases',
                'Other secondary pulmonary hypertension',
                'Scoliosis, unspecified',
                'Scoliosis, unspecified Site unspecified',
                'Sleep apnoea',
            ]
        }
        # Create a new column 'Category' based on the provided categories
        diagnoses['Category'] = diagnoses['diagnosis'].apply(lambda x: next((category for category, values in categories.items() if x in values), 'Other'))  

        #sub-categories
        categories = {
            'Cardiac Malformations': [
                'Atrial septal defect',
                'Atrioventricular septal defect',
                'Coarctation of aorta',
            ],
            'Valve-related conditions': [
                'Congenital insufficiency of aortic valve',
                'Congenital pulmonary valve stenosis',
                'Congenital stenosis of aortic valve',
                'Congenital tricuspid stenosis',
            ], 
                'Congenital Heart Anomalies': [
                    'Ebstein anomaly',
                    'Hypoplastic left heart syndrome',
                    'Malformation of coronary vessels',
                    'Other congenital malformations of aorta',
                    'Other congenital malformations of great veins',
                    'Other congenital malformations of pulmonary artery',
                    'Other specified congenital malformations of heart',
            ],
            'Cardiac Devices and Implants': [
                'Adjustment and management of cardiac devices',
                'Adjustment and management of vascular access device',
                'Other specified complications of cardiac and vascular prosthetic devices, implants, and grafts',
            ],
            ' Cardiomyopathies': [
                'Other cardiomyopathies',
            ],
            'Heart Transplantation': [
                'Heart transplant failure and rejection',
                'Heart transplant status',
            ],
            ' Pulmonary Hypertension': [
            'Other specified diseases of pulmonary vessels',
                'Primary pulmonary hypertension',
                'Stenosis of pulmonary artery',
            ],
            'Ventricular Conditions': [
                'Ventricular premature depolarization',
                'Ventricular septal defect',
                'Ventricular tachycardia',
            ],
            'Aortic Conditions': [
                'Thoracic aortic aneurysm, without mention of rupture',
            ],
            'Tetralogy of Fallot': [
                'Tetralogy of Fallot'
            ]
        } 
            
        diagnoses['CVD_sub_category'] = diagnoses['diagnosis'].apply(lambda x: next((category for category, values in categories.items() if x in values), 'N/A'))
               
        diagnoses=diagnoses.drop_duplicates()
        return diagnoses 
    
    def load_labs(self):
   # Load configuration from config.json
        with open('medtimeline/config.json', 'r') as json_file:
            config = json.load(json_file)

        # Construct the full path to the 'Data' folder and 'csv_file_name'
        labs_csv_path = config['Paths']['labs_csv_path']

        # Load the CSV file
        labs = pd.read_csv(labs_csv_path)

        labs=labs.rename(columns={
            'SpecimenType':'specimen_type',
            'start_datetime':'lab_date',
            'end_datetime':'end_date',
            'SpecimenSource':'specimen_source',
            'PathologyType':'pathology_type',
            'SourceType':'patient_class',
            'LabTestKey':'lab_test_key',
            'NumericValue':'value',
            'Section':'section',
            'SubSection':'subsection',
            'Method':'method',
            'collected_datetime':'end_date_labs',
            'recieved_datetime':'recieved_date',
            'verified_datetime':'verified_date'
            ,'TestName':'test_name',
            'Unit':'unit'
            })
        
        labs['flag'] = labs['flag'].fillna('Normal')
        labs["code"] = labs["component_basename"] + labs["flag"]
        labs=labs.drop(['end_date','lab_date'],axis=1)

        return labs

    def load_admissions(self):
   # Load configuration from config.json
        with open('medtimeline/config.json', 'r') as json_file:
            config = json.load(json_file)

        # Construct the full path to the 'Data' folder and 'csv_file_name'
        admissions_csv_path = config['Paths']['admissions_csv_path']

        # Load the CSV file
        admissions = pd.read_csv(admissions_csv_path)

        admissions=admissions.rename(columns={'start_datetime':'admission_date','end_datetime':'discharge_date'})
        admissions.set_index(['project_id','admission_date']).sort_index()
        #calculate length of stay
         # Note: The Python timedelta object considers 24 hours as one day

        admissions['admission_date'] = pd.to_datetime(admissions['admission_date'],format='mixed')
        admissions['discharge_date'] = pd.to_datetime(admissions['discharge_date'],format='mixed')
    
        admissions['los_d'] = admissions['discharge_date'] - admissions['admission_date']
        admissions.drop_duplicates()

        #assign unique ID to each admission

        admissions = admissions.assign(admission_id = np.nan)
        pr_counts = admissions.project_id.value_counts()
        for pr in admissions.project_id.unique():
            admissions.loc[admissions['project_id'] == pr,'admission_id'] = list(range(pr_counts.loc[pr]))

        admissions['admission_id'] = admissions['admission_id'].astype(int) + 1
        admissions['admission_id'] = admissions['project_id'].astype(str) +'_'+ admissions['admission_id'].astype(str)
        return admissions
    

#Individual timeline generators

    def generate_surgery_timeline(self):
        surgery=self.load_surgery()
        admissions = self.load_admissions()
        surgery = surgery.merge(admissions, on='project_id', how='inner')

            # Convert date columns to datetime objects
        surgery['discharge_date'] = pd.to_datetime(surgery['discharge_date'])
        surgery['end_date_surg'] = pd.to_datetime(surgery['end_date_surg'])

        # Group by 'admission_id' and filter rows
        filtered_surg = surgery.groupby('admission_id').apply(lambda group: group[group['end_date_surg'] <= group['discharge_date']])

        # Reset the index and drop the group and level_1 columns
        filtered_surg.reset_index(level=0, drop=True, inplace=True)

        # Convert date columns to datetime objects
        filtered_surg['discharge_date'] = pd.to_datetime(filtered_surg['discharge_date'])
        filtered_surg['end_date_surg'] = pd.to_datetime(filtered_surg['end_date_surg'])

        result_df_surg_list = []

        # Iterate through unique admission_ids
        for admission_id in filtered_surg['admission_id'].unique():
            # Filter the DataFrame for the current admission_id
            project_df_surg = filtered_surg[filtered_surg['admission_id'] == admission_id].copy()

            # Sort the DataFrame by 'end_date_meds' in ascending order
            project_df_surg.sort_values(by='end_date_surg', inplace=True)

            # Calculate the number of days for each 'end_date_meds' within the range
            project_df_surg['Day'] = (project_df_surg['discharge_date'] - project_df_surg['end_date_surg']).dt.days + 1

            result_df_surg_list.append(project_df_surg)

        # Use pd.concat to concatenate the list of DataFrames vertically
        result_df_surg = pd.concat(result_df_surg_list, ignore_index=True)

        # Reset the index
        result_df_surg.reset_index(drop=True, inplace=True)

        result_df_surg['Day'] = result_df_surg['Day'].astype(str)

        # Group by 'admission_id' and 'Day' and collect 'code' values as a list
        custom_column_order_surg = sorted(result_df_surg['Day'].unique(), key=lambda x: int(x.split()[-1]))

        # Group by 'admission_id' and 'Day' and collect 'code' values as a list
        grouped_surg = result_df_surg.groupby(['admission_id', 'Day'])['code'].apply(list).reset_index()

        # Pivot the DataFrame and specify the custom column order
        pivoted_df_surg = grouped_surg.pivot(index='admission_id', columns='Day', values='code')[custom_column_order_surg].reset_index()
        
        return pivoted_df_surg
    
    def generate_medication_timeline(self):
        med = self.load_med()
        admissions = self.load_admissions()
        med = med.merge(admissions, on='project_id', how='inner')

        # Convert date columns to datetime objects
        med['discharge_date'] = pd.to_datetime(med['discharge_date'])
        med['end_date_meds'] = pd.to_datetime(med['end_date_meds'])

        # Group by 'admission_id' and filter rows
        filtered_med = med.groupby('admission_id').apply(lambda group: group[group['end_date_meds'] <= group['discharge_date']])

        # Reset the index and drop the group and level_1 columns
        filtered_med.reset_index(level=0, drop=True, inplace=True)

        # Convert date columns to datetime objects
        filtered_med['discharge_date'] = pd.to_datetime(filtered_med['discharge_date'])
        filtered_med['end_date_meds'] = pd.to_datetime(filtered_med['end_date_meds'])

        #Initialize an empty list to store DataFrames
        result_df_med_list = []

        # Iterate through unique admission_ids
        for admission_id in filtered_med['admission_id'].unique():
            # Filter the DataFrame for the current admission_id
            project_df_med = filtered_med[filtered_med['admission_id'] == admission_id].copy()

            # Sort the DataFrame by 'end_date_meds' in ascending order
            project_df_med.sort_values(by='end_date_meds', inplace=True)

            # Calculate the number of days for each 'end_date_meds' within the range
            project_df_med['Day'] = (project_df_med['discharge_date'] - project_df_med['end_date_meds']).dt.days + 1

            result_df_med_list.append(project_df_med)

        # Use pd.concat to concatenate the list of DataFrames vertically
        result_df_med = pd.concat(result_df_med_list, ignore_index=True)

        # Reset the index
        result_df_med.reset_index(drop=True, inplace=True)

        result_df_med['Day'] = result_df_med['Day'].astype(str)

        # Group by 'admission_id' and 'Day' and collect 'code' values as a list
        custom_column_order_med = sorted(result_df_med['Day'].unique(), key=lambda x: int(x.split()[-1]))

        # Group by 'admission_id' and 'Day' and collect 'code' values as a list
        grouped_med = result_df_med.groupby(['admission_id', 'Day'])['code'].apply(list).reset_index()

        # Pivot the DataFrame and specify the custom column order
        pivoted_df_med = grouped_med.pivot(index='admission_id', columns='Day', values='code')[custom_column_order_med].reset_index()

        return pivoted_df_med  # Return the DataFrame


    def generate_diagnoses_timeline(self):
        diagnoses=self.load_diagnoses()
        admissions = self.load_admissions()
        diagnoses = diagnoses.merge(admissions, on='project_id', how='inner')

        # Convert date columns to datetime objects
        diagnoses['discharge_date'] = pd.to_datetime(diagnoses['discharge_date'])
        diagnoses['end_date_diag'] = pd.to_datetime(diagnoses['end_date_diag'])

        # Group by 'admission_id' and filter rows
        filtered_diag = diagnoses.groupby('admission_id').apply(lambda group: group[group['end_date_diag'] <= group['discharge_date']])

        # Reset the index and drop the group and level_1 columns
        filtered_diag.reset_index(level=0, drop=True, inplace=True)

        # Convert date columns to datetime objects
        filtered_diag['discharge_date'] = pd.to_datetime(filtered_diag['discharge_date'])
        filtered_diag['end_date_diag'] = pd.to_datetime(filtered_diag['end_date_diag'])

        # Initialize an empty list to store the results
        result_df_diag_list=[]

        # Iterate through unique admission_ids
        for admission_id in filtered_diag['admission_id'].unique():
            # Filter the DataFrame for the current admission_id
            project_df = filtered_diag[filtered_diag['admission_id'] == admission_id].copy()

            # Sort the DataFrame by 'end_date_meds' in ascending order
            project_df.sort_values(by='end_date_diag', inplace=True)

            # Calculate the number of days for each 'end_date_meds' within the range
            project_df['Day'] = (project_df['discharge_date'] - project_df['end_date_diag']).dt.days + 1

            # Append the results for the current admission_id to the result DataFrame

            result_df_diag_list.append(project_df_diag)

        # Use pd.concat to concatenate the list of DataFrames vertically
        result_df_diag = pd.concat(result_df_diag_list, ignore_index=True)

        # Reset the index
        result_df_diag.reset_index(drop=True, inplace=True)

        result_df_diag['Day'] = result_df_diag['Day'].astype(str)

        # Group by 'admission_id' and 'Day' and collect 'code' values as a list
        custom_column_order_diag = sorted(result_df_diag['Day'].unique(), key=lambda x: int(x.split()[-1]))

        # Group by 'admission_id' and 'Day' and collect 'code' values as a list
        grouped_diag = result_df_diag.groupby(['admission_id', 'Day'])['code'].apply(list).reset_index()

        # Pivot the DataFrame and specify the custom column order
        pivoted_df_diag = grouped_diag.pivot(index='admission_id', columns='Day', values='code')[custom_column_order_diag].reset_index()
        
        return pivoted_df_diag

        
    def generate_labs_timeline(self):
        labs=self.load_labs()
        labs = self.load_labs()
        labs = labs.merge(admissions, on='project_id', how='inner')

            # Convert date columns to datetime objects
        labs['discharge_date'] = pd.to_datetime(labs['discharge_date'])
        labs['end_date_labs'] = pd.to_datetime(labs['end_date_labs'])

        # Group by 'admission_id' and filter row so that collection dates later than the discharge date are not included
        filtered_labs = labs.groupby('admission_id').apply(lambda group: group[group['end_date_labs'] <= group['discharge_date']])

        # Reset the index and drop the group and level_1 columns
        filtered_labs.reset_index(level=0, drop=True, inplace=True)

        # Convert date columns to datetime objects
        filtered_labs['discharge_date'] = pd.to_datetime(filtered_labs['discharge_date'])
        filtered_labs['end_date_labs'] = pd.to_datetime(filtered_labs['end_date_labs'])

        # Initialize an empty listto store the results
        result_df_labs_list = []

        # Iterate through unique admission_ids
        for admission_id in filtered_labs['admission_id'].unique():
            # Filter the DataFrame for the current admission_id
            project_df = filtered_labs[filtered_labs['admission_id'] == admission_id].copy()

            # Sort the DataFrame by 'end_date_meds' in ascending order
            project_df.sort_values(by='end_date_labs', inplace=True)

            # Calculate the number of days for each 'end_date_meds' within the range
            project_df['Day'] = (project_df['discharge_date'] - project_df['end_date_labs']).dt.days + 1

            # Append the results for the current admission_id to the result DataFrame

            result_df_labs_list.append(project_df_labs)

        # Use pd.concat to concatenate the list of DataFrames vertically
        result_df_labs = pd.concat(result_df_labs_list, ignore_index=True)

        # Reset the index
        result_df_labs.reset_index(drop=True, inplace=True)

        result_df_labs['Day'] = result_df_labs['Day'].astype(str)

        # Group by 'admission_id' and 'Day' and collect 'code' values as a list
        custom_column_order_labs = sorted(result_df_labs['Day'].unique(), key=lambda x: int(x.split()[-1]))

        # Group by 'admission_id' and 'Day' and collect 'code' values as a list
        grouped_labs = result_df_labs.groupby(['admission_id', 'Day'])['code'].apply(list).reset_index()

        # Pivot the DataFrame and specify the custom column order
        pivoted_df_labs = grouped_labs.pivot(index='admission_id', columns='Day', values='code')[custom_column_order_labs].reset_index()
        
        return pivoted_df_labs


class ProceduresTimelineGenerator:
    def __init__(self, config_path):
        # Read the configuration from the JSON file
        with open(config_path, 'r') as json_file:
            config = json.load(json_file)
        
        # Store the configuration values as class attributes
        self.data_path = config['Paths']['data_path']

    def load_echo(self):
   # Load configuration from config.json
        with open('medtimeline/config.json', 'r') as json_file:
            config = json.load(json_file)

        # Construct the full path to the 'Data' folder and 'csv_file_name'
        echo_csv_path = config['Paths']['echo_csv_path']

        with open((echo_csv_path), 'rb') as f:
            result = chardet.detect(f.read())  # or readline if the file is large 
            encoding = result['encoding']
        
        echo= pd.read_csv(echo_csv_path, encoding=encoding)

        echo=echo.rename(columns={
            'start_datetime':'start_date',
            'end_datetime':'end_date',
            'ImagingKey':'code',
            'EchoFindingKey':'echo_finding_key'
            })
        
        echo=echo[['project_id','end_date','code','procedure_name']]

        echo['end_date']=pd.to_datetime(echo['end_date']).dt.date    
        echo['end_date']=pd.to_datetime(echo['end_date']).dt.date

        return echo
    
    def load_radiology(self):
    # Load configuration from config.json
        with open('medtimeline/config.json', 'r') as json_file:
            config = json.load(json_file)

        # Construct the full path to the 'Data' folder and 'csv_file_name'
        radiology_csv_path = config['Paths']['radiology_csv_path']

        # Load the CSV file
        radiology = pd.read_csv(radiology_csv_path)

        radiology=radiology.rename(columns={
            'procedure_code':'code',
            'start_datetime':'start_date',
            'end_datetime':'end_date',
            'canceled_datetime':'canceled_date'
            })
        
        radiology=radiology[['project_id','end_date','code','procedure_name']]
        radiology['end_date']=pd.to_datetime(radiology['end_date']).dt.date

        return radiology
    
    def load_procedure_components(self):
   # Load configuration from config.json
        with open('medtimeline/config.json', 'r') as json_file:
            config = json.load(json_file)

        # Construct the full path to the 'Data' folder and 'csv_file_name'
        procedure_components_csv_path = config['Paths']['procedure_components_csv_path']

        # Load the CSV file
        PC = pd.read_csv(procedure_components_csv_path)

        PC=PC.rename(columns={
            'collected_datetime':'end_date',
            'ProcedureCode':'code',
            'ProcedureEventKey':'procedure_event_code',
            'ProcedureEpicId':'procedure_epic_id',
            'ProcedureCategory':'procedure_category',
            'ProcedureName':'procedure_name'
            })
        
        PC=PC[['project_id','end_date','code','ProcedureName']]
        
        PC['end_date'] = pd.to_datetime(PC['end_date'])
        PC['end_date']=pd.to_datetime(PC['end_date']).dt.date

        return PC
    
    def load_procedure(self):
   # Load configuration from config.json
        with open('medtimeline/config.json', 'r') as json_file:
            config = json.load(json_file)

        # Construct the full path to the 'Data' folder and 'csv_file_name'
        procedures_csv_path = config['Paths']['procedures_csv_path']

        # Load the CSV file

        with open((procedures_csv_path), 'rb') as f:
            result = chardet.detect(f.read())  # or readline if the file is large 
            encoding = result['encoding']
        
        procedures = pd.read_csv(procedures_csv_path, encoding=encoding)

        procedures=procedures.rename(columns={
            'start_datetime':'start_date',
            'end_datetime':'end_date',
            'proc_nat_code':'code',
            'proc_name':'procedure_name'
            })
        
        procedures=procedures.drop('proc_local_code',axis=1)
        procedures=procedures[['project_id','end_date','code','proc_name']]
        procedures['end_date'] = pd.to_datetime(procedures['end_date'])
        procedures['end_date']=pd.to_datetime(procedures['end_date']).dt.date

        return procedures 
    
    
    def load_procedures(self):
        echo=self.load_echo()
        radiology=self.load_radiology()
        PC=self.load_procedure_components()
        procedures=self.load_procedure() 
        admissions = self.load_admissions()

        combined_df = pd.concat([radiology, procedures, PC], ignore_index=True)


        procedures_final=pd.merge(combined_df, echo, on=['project_id','end_date','procedure_name'], how='left')
        procedures_final=procedures_final.drop_duplicates()

        procedures_final=procedures_final[['project_id','end_date','code_x','procedure_name']]
        procedures_final=procedures_final.rename(columns={'code_x':'code','end_date':'end_date_proc'})
        procedures_final=procedures_final.merge(admissions, on='project_id',how='inner')

        return procedures_final
    
    def generate_procedure_timeline(self):
        procedures=self.load_procedures()

        # Convert date columns to datetime objects
        procedures['discharge_date'] = pd.to_datetime(procedures['discharge_date'])
        procedures['end_date_proc'] = pd.to_datetime(procedures['end_date_proc'])

        # Group by 'admission_id' and filter rows
        filtered_proc = procedures.groupby('admission_id').apply(lambda group: group[group['end_date_proc'] <= group['discharge_date']])

        # Reset the index and drop the group and level_1 columns
        filtered_proc.reset_index(level=0, drop=True, inplace=True)

        # Convert date columns to datetime objects
        filtered_proc['discharge_date'] = pd.to_datetime(filtered_proc['discharge_date'])
        filtered_proc['end_date_proc'] = pd.to_datetime(filtered_proc['end_date_proc'])

        # Initialize an empty list to store the results
        result_df_proc_list = []

        # Iterate through unique admission_ids
        for admission_id in filtered_proc['admission_id'].unique():
            # Filter the DataFrame for the current admission_id
            project_df = filtered_proc[filtered_proc['admission_id'] == admission_id].copy()

            # Sort the DataFrame by 'end_date_meds' in ascending order
            project_df.sort_values(by='end_date_proc', inplace=True)

            # Calculate the number of days for each 'end_date_meds' within the range
            project_df['Day'] = (project_df['discharge_date'] - project_df['end_date_proc']).dt.days + 1

            # Append the results for the current admission_id to the result DataFrame

            result_df_proc_list.append(project_df_proc)

        # Use pd.concat to concatenate the list of DataFrames vertically
        result_df_proc = pd.concat(result_df_proc_list, ignore_index=True)

        # Reset the index
        result_df_proc.reset_index(drop=True, inplace=True)

        result_df_proc['Day'] = result_df_proc['Day'].astype(str)

        # Group by 'admission_id' and 'Day' and collect 'code' values as a list
        custom_column_order_proc = sorted(result_df_proc['Day'].unique(), key=lambda x: int(x.split()[-1]))

        # Group by 'admission_id' and 'Day' and collect 'code' values as a list
        grouped_proc = result_df_proc.groupby(['admission_id', 'Day'])['code'].apply(list).reset_index()

        # Pivot the DataFrame and specify the custom column order
        pivoted_df_proc = grouped_proc.pivot(index='admission_id', columns='Day', values='code')[custom_column_order_proc].reset_index()
        return pivoted_df_proc

class PatientJourneyGenerator:
    def __init__(self, config_path):
        # Read the configuration from the JSON file
        with open(config_path, 'r') as json_file:
            config = json.load(json_file)
        
        # Store the configuration values as class attributes
        self.data_path = config['Paths']['data_path']

    def GenerateFullJourney(self):
        timeline_generator = TimelineGenerator(config_path)

        med = timeline_generator.generate_medication_timeline()
        surgery = timeline_generator.generate_surgery_timeline()
        labs = timeline_generator.generate_labs_timeline()
        diagnoses = timeline_generator.generate_diagnoses_timeline()

        timeline_generator_procedures = ProceduresTimelineGenerator(config_path)
    
        procedures = timeline_generator_procedures.generate_procedure_timeline()

        merged_df = pd.concat([med, surgery, labs, diagnoses, procedures])
        grouped_df = merged_df.groupby('admission_id').agg(lambda x: list(x))
        grouped_df.reset_index(inplace=True)

        return grouped_df


