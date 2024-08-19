from flask import Flask, jsonify, request, send_file, send_from_directory, redirect, url_for
from flask_cors import CORS
import pandas as pd
import json
import os
import numpy as np
import random
import plotly
import plotly.express as px
import plotly.io as pio
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import requests

app = Flask(__name__, static_folder='/Users/alan/arc-dataPortalFinal/frontend/dist')

# Enable CORS for all domains on all routes
CORS(app, resources={r"/*": {"origins": "http://192.168.127.128:4173"}})


pio.templates.default = "plotly_white"

TODAY = datetime.date.today()

app.config['LANGUAGE'] = 'ENG'
app.config['USER_NAME'] = '102'
app.config['STUDY_NAME'] = 'nagoya'

response = requests.get('https://xs111291.xsrv.jp/Arc/Data/GetPatientDataForPatientID.php?patientID=' + app.config['USER_NAME'])
USER_DATA = response.json()
today = datetime.datetime.today().date()
birthday = datetime.datetime.strptime(USER_DATA['USER_DOB'], "%Y-%m-%d").date()
USER_DATA['USER_AGE'] = today.year - birthday.year
if (today.month, today.day) < (birthday.month, birthday.day):
        USER_DATA['USER_AGE'] -= 1

PHP_URL = 'https://xs111291.xsrv.jp/Arc/Data/GetMetricResultsForSession.php?studyID=' + app.config['STUDY_NAME'] + '&sessionID='
response = requests.get(PHP_URL+app.config['USER_NAME'])
responseJSON = response.json()
USER_METRICS = response.json()['results']
USER_DATA['SESSION_DATE'] = response.json()['SESSION_DATE']

headers_labels = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/headers_labels.csv')
HEADERS_LABELS = {
    'DEMOGRAPHICS': {
        'DOB': headers_labels['Demographics'].iloc[0],
        'AGE': headers_labels['Demographics'].iloc[1],
        'SEX': headers_labels['Demographics'].iloc[2],
        'SESS_DATE': headers_labels['Demographics'].iloc[3],
        'SESS_ID': headers_labels['Demographics'].iloc[4],
        'PLAYER_ID': headers_labels['Demographics'].iloc[5],
    },
    'BUTTONS': {
        'PRINT_REPORT': headers_labels['Buttons'].iloc[0],
        'ADD_SESSION': headers_labels['Buttons'].iloc[1],
        'EXPORT_CSV': headers_labels['Buttons'].iloc[2],
    },
    'TAB_NAMES': {
        'OVERVIEW': headers_labels['Tab Names'].iloc[0],
        'PSYCHOTHERAPY_SUGGESTIONS': headers_labels['Tab Names'].iloc[1],
        'PERSONALIZED_SUGGESTIONS': headers_labels['Tab Names'].iloc[2],
        'ABOUT_METRICS': headers_labels['Tab Names'].iloc[3],
    },
    'METRIC_CATEGORIES': {
        'COMPLEX_COGNITIVE_FUNCTIONS': headers_labels['Metric Categories'].iloc[0],
        'SIMPLER_COGNITIVE_FUNCTIONS': headers_labels['Metric Categories'].iloc[1],
    },
    'SECTION_NAMES': {
        'FOR_DOCTORS': headers_labels['Section Names'].iloc[0],
        'PERFORMANCE_PLOT': headers_labels['Section Names'].iloc[1],
        'SCORE_TABLE': headers_labels['Section Names'].iloc[2],
        'DATA_SUMMARY': headers_labels['Section Names'].iloc[3],
    },
    'CHART_LABELS': {
        'LINE_CHART': headers_labels['Chart Labels'].iloc[0],
        'RADAR_CHART': headers_labels['Chart Labels'].iloc[1],
        'RESULTS_FOR': headers_labels['Chart Labels'].iloc[2],
        'LEGEND': headers_labels['Chart Labels'].iloc[3],
        'STRENGTH': headers_labels['Chart Labels'].iloc[4],
        'WEAKNESS': headers_labels['Chart Labels'].iloc[5],
    },
    'TABLE_LABELS': {
        'METRIC': headers_labels['Table Labels'].iloc[0],
        'FULL_NAME': headers_labels['Table Labels'].iloc[1],
        'CODE': headers_labels['Table Labels'].iloc[2],
        'RAW_VALUE': headers_labels['Table Labels'].iloc[3],
        'AVERAGE': headers_labels['Table Labels'].iloc[4],
        'T_SCORE': headers_labels['Table Labels'].iloc[5],
    },
}

EXPORT_COLS = ['sessionID', 'metricName', 'metricIdentifier', 'rawValue', 'scoredValue', 'zScoreInSample', 'zScoreInPopulation', 'tScoreInSample', 'tScoreInPopulation', 'metricTitle']
USER_NAME = USER_DATA['USER_NAME']

MetricInfo = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/metric_info.csv')
Averages = pd.read_csv('src/data/Population_Metrics.csv')
PrimaryMetrics = pd.read_csv('src/data/AllMetrics.csv')
# UserMetrics = PrimaryMetrics[PrimaryMetrics['sessionID'] == USER_NAME].round(2)
# UserMetrics[EXPORT_COLS].to_csv(f'src/content/{app.config['LANGUAGE']}/results/{USER_NAME}_UserMetrics.csv')

metrics = ['EFCS', 'TACR', 'MDS', 'SAD', 'SAR', 'SAV']
for metric in metrics:
    USER_METRICS[metric]['rawValue'] = round(USER_METRICS[metric]['rawValue'], 2)
    USER_METRICS[metric]['zScore'] = round(USER_METRICS[metric]['zScore'], 2)
    USER_METRICS[metric]['tScore'] = round(USER_METRICS[metric]['tScore'], 2)
    USER_METRICS[metric]['metricFull'] = MetricInfo[MetricInfo['metricName'] == metric]['fullName'].iloc[0]
    USER_METRICS[metric]['metricLayman'] = MetricInfo[MetricInfo['metricName'] == metric]['laymansName'].iloc[0]
    USER_METRICS[metric]['metricDesc'] = MetricInfo[MetricInfo['metricName'] == metric]['description'].iloc[0]
    USER_METRICS[metric]['metricQuickDesc'] = MetricInfo[MetricInfo['metricName'] == metric]['quickDesc'].iloc[0]
    USER_METRICS[metric]['metricAverage'] = Averages[Averages['metricName'] == metric]['meanPopulation'].iloc[0]

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/u=<u_name>')
def set_user(u_name):
    app.config['USER_NAME'] = u_name
    response = requests.get('https://xs111291.xsrv.jp/Arc/Data/GetPatientDataForPatientID.php?patientID=' + app.config['USER_NAME'])
    USER_DATA = response.json()
    today = datetime.datetime.today().date()
    birthday = datetime.datetime.strptime(USER_DATA['USER_DOB'], "%Y-%m-%d").date()
    USER_DATA['USER_AGE'] = today.year - birthday.year
    if (today.month, today.day) < (birthday.month, birthday.day):
            USER_DATA['USER_AGE'] -= 1

    PHP_URL = 'https://xs111291.xsrv.jp/Arc/Data/GetMetricResultsForSession.php?studyID=' + app.config['STUDY_NAME'] + '&sessionID='
    response = requests.get(PHP_URL+app.config['USER_NAME'])
    responseJSON = response.json()
    USER_METRICS = response.json()['results']
    USER_DATA['SESSION_DATE'] = response.json()['SESSION_DATE']
    
    for metric in metrics:
        USER_METRICS[metric]['rawValue'] = round(USER_METRICS[metric]['rawValue'], 2)
        USER_METRICS[metric]['zScore'] = round(USER_METRICS[metric]['zScore'], 2)
        USER_METRICS[metric]['tScore'] = round(USER_METRICS[metric]['tScore'], 2)
        USER_METRICS[metric]['metricFull'] = MetricInfo[MetricInfo['metricName'] == metric]['fullName'].iloc[0]
        USER_METRICS[metric]['metricLayman'] = MetricInfo[MetricInfo['metricName'] == metric]['laymansName'].iloc[0]
        USER_METRICS[metric]['metricDesc'] = MetricInfo[MetricInfo['metricName'] == metric]['description'].iloc[0]
        USER_METRICS[metric]['metricQuickDesc'] = MetricInfo[MetricInfo['metricName'] == metric]['quickDesc'].iloc[0]
        USER_METRICS[metric]['metricAverage'] = Averages[Averages['metricName'] == metric]['meanPopulation'].iloc[0]

    
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/s=<s_name>')
def set_study(s_name):
    app.config['STUDY_NAME'] = s_name
    response = requests.get('https://xs111291.xsrv.jp/Arc/Data/GetPatientDataForPatientID.php?patientID=' + app.config['USER_NAME'])
    USER_DATA = response.json()
    today = datetime.datetime.today().date()
    birthday = datetime.datetime.strptime(USER_DATA['USER_DOB'], "%Y-%m-%d").date()
    USER_DATA['USER_AGE'] = today.year - birthday.year
    if (today.month, today.day) < (birthday.month, birthday.day):
            USER_DATA['USER_AGE'] -= 1

    PHP_URL = 'https://xs111291.xsrv.jp/Arc/Data/GetMetricResultsForSession.php?studyID=' + app.config['STUDY_NAME'] + '&sessionID='
    response = requests.get(PHP_URL+app.config['USER_NAME'])
    responseJSON = response.json()
    USER_METRICS = response.json()['results']
    USER_DATA['SESSION_DATE'] = response.json()['SESSION_DATE']
    
    metrics = ['EFCS', 'TACR', 'MDS', 'SAD', 'SAR', 'SAV']
    for metric in metrics:
        USER_METRICS[metric]['rawValue'] = round(USER_METRICS[metric]['rawValue'], 2)
        USER_METRICS[metric]['zScore'] = round(USER_METRICS[metric]['zScore'], 2)
        USER_METRICS[metric]['tScore'] = round(USER_METRICS[metric]['tScore'], 2)
        USER_METRICS[metric]['metricFull'] = MetricInfo[MetricInfo['metricName'] == metric]['fullName'].iloc[0]
        USER_METRICS[metric]['metricLayman'] = MetricInfo[MetricInfo['metricName'] == metric]['laymansName'].iloc[0]
        USER_METRICS[metric]['metricDesc'] = MetricInfo[MetricInfo['metricName'] == metric]['description'].iloc[0]
        USER_METRICS[metric]['metricQuickDesc'] = MetricInfo[MetricInfo['metricName'] == metric]['quickDesc'].iloc[0]
        USER_METRICS[metric]['metricAverage'] = Averages[Averages['metricName'] == metric]['meanPopulation'].iloc[0]

    
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/lang=<language_code>')
def set_language(language_code):
    # Update the LANGUAGE configuration based on URL parameter
    valid_languages = ['ENG', 'JPN']
    language_code = language_code.upper()
    if language_code in valid_languages:
        app.config['LANGUAGE'] = language_code
        # Redirect to the homepage after updating the language
        
        headers_labels = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/headers_labels.csv')
        HEADERS_LABELS = {
            'DEMOGRAPHICS': {
                'DOB': headers_labels['Demographics'].iloc[0],
                'AGE': headers_labels['Demographics'].iloc[1],
                'SEX': headers_labels['Demographics'].iloc[2],
                'SESS_DATE': headers_labels['Demographics'].iloc[3],
                'SESS_ID': headers_labels['Demographics'].iloc[4],
                'PLAYER_ID': headers_labels['Demographics'].iloc[5],
            },
            'BUTTONS': {
                'PRINT_REPORT': headers_labels['Buttons'].iloc[0],
                'ADD_SESSION': headers_labels['Buttons'].iloc[1],
                'EXPORT_CSV': headers_labels['Buttons'].iloc[2],
            },
            'TAB_NAMES': {
                'OVERVIEW': headers_labels['Tab Names'].iloc[0],
                'PSYCHOTHERAPY_SUGGESTIONS': headers_labels['Tab Names'].iloc[1],
                'PERSONALIZED_SUGGESTIONS': headers_labels['Tab Names'].iloc[2],
                'ABOUT_METRICS': headers_labels['Tab Names'].iloc[3],
            },
            'METRIC_CATEGORIES': {
                'COMPLEX_COGNITIVE_FUNCTIONS': headers_labels['Metric Categories'].iloc[0],
                'SIMPLER_COGNITIVE_FUNCTIONS': headers_labels['Metric Categories'].iloc[1],
            },
            'SECTION_NAMES': {
                'FOR_DOCTORS': headers_labels['Section Names'].iloc[0],
                'PERFORMANCE_PLOT': headers_labels['Section Names'].iloc[1],
                'SCORE_TABLE': headers_labels['Section Names'].iloc[2],
                'DATA_SUMMARY': headers_labels['Section Names'].iloc[3],
            },
            'CHART_LABELS': {
                'LINE_CHART': headers_labels['Chart Labels'].iloc[0],
                'RADAR_CHART': headers_labels['Chart Labels'].iloc[1],
                'RESULTS_FOR': headers_labels['Chart Labels'].iloc[2],
                'LEGEND': headers_labels['Chart Labels'].iloc[3],
                'STRENGTH': headers_labels['Chart Labels'].iloc[4],
                'WEAKNESS': headers_labels['Chart Labels'].iloc[5],
            },
            'TABLE_LABELS': {
                'METRIC': headers_labels['Table Labels'].iloc[0],
                'FULL_NAME': headers_labels['Table Labels'].iloc[1],
                'CODE': headers_labels['Table Labels'].iloc[2],
                'RAW_VALUE': headers_labels['Table Labels'].iloc[3],
                'AVERAGE': headers_labels['Table Labels'].iloc[4],
                'T_SCORE': headers_labels['Table Labels'].iloc[5],
            },
        }

        EXPORT_COLS = ['sessionID', 'metricName', 'metricIdentifier', 'rawValue', 'scoredValue', 'zScoreInSample', 'zScoreInPopulation', 'tScoreInSample', 'tScoreInPopulation', 'metricTitle']
        USER_NAME = USER_DATA['USER_NAME']

        MetricInfo = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/metric_info.csv')
        Averages = pd.read_csv('src/data/Population_Metrics.csv')
        
        # Assigning Strengths/Weaknesses (Stars/Diamonds)
        CCF_threshold = 10
        SCF_threshold = 1

        DIAMOND_CCF, STAR_CCF, DIAMOND_SCF, STAR_SCF = getSymbols(CCF_threshold, SCF_threshold)

        NAME = USER_DATA['USER_NAME']
        ratings = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/ratings.csv', header = None).iloc[0].tolist()
        rating_map = {
            'VERY LOW': ratings[0],
            'LOW': ratings[1],
            'AVERAGE': ratings[2],
            'HIGH': ratings[3],
            'VERY HIGH': ratings[4]
        }
        EF_RAW = USER_METRICS['EFCS']['rawValue']

        EF_RATING = rating_map[USER_METRICS['EFCS']['scoreRating']]
        TACR_RATING = rating_map[USER_METRICS['TACR']['scoreRating']]
        MDS_RATING = rating_map[USER_METRICS['MDS']['scoreRating']]
        SAR_RATING = rating_map[USER_METRICS['SAR']['scoreRating']]
        SAD_RATING = rating_map[USER_METRICS['SAD']['scoreRating']]
        SAV_RATING = rating_map[USER_METRICS['SAV']['scoreRating']]

        EF_T_SCORE = USER_METRICS['EFCS']['tScore']
        TACR_T_SCORE = USER_METRICS['TACR']['tScore']
        MDS_T_SCORE = USER_METRICS['MDS']['tScore']
        SAR_T_SCORE = USER_METRICS['SAR']['tScore']
        SAD_T_SCORE = USER_METRICS['SAD']['tScore']
        SAV_T_SCORE = USER_METRICS['SAV']['tScore']

        with open(f'src/content/{app.config['LANGUAGE']}/results/pre_data_summary.md', 'r') as file:
            pre_data_summary = file.read()

        relative_results = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/results/relative_results.csv')
        print(DIAMOND_CCF, STAR_CCF, DIAMOND_SCF, STAR_SCF)

        # CCF
        if(DIAMOND_CCF != None and STAR_CCF != None):
            if (EF_RATING == 'LOW' or EF_RATING == 'VERY LOW'):
                CCF_REL = relative_results['low'].iloc[0]
            elif (EF_RATING == 'AVERAGE'):
                CCF_REL = relative_results['average'].iloc[0]
            else: # EF_RATING == 'HIGH' or 'VERY HIGH'
                CCF_REL = relative_results['high'].iloc[0]
        else:
            CCF_REL = ""
        # SCF
        if(DIAMOND_SCF != None and STAR_SCF != None):
            if (EF_RATING == 'LOW' or EF_RATING == 'VERY LOW'):
                SCF_REL = relative_results['low'].iloc[1]
            elif (EF_RATING == 'AVERAGE'):
                SCF_REL = relative_results['average'].iloc[1]
            else: # EF_RATING == 'HIGH' or 'VERY HIGH'
                SCF_REL = relative_results['high'].iloc[1]
        else:
            SCF_REL = ""

        CCF_RELATIVE = eval(f'f"""{CCF_REL}"""')
        SCF_RELATIVE = eval(f'f"""{SCF_REL}"""')
        print(CCF_RELATIVE, SCF_RELATIVE)

            # replacing values w/ variables
        pre_data_summary = eval(f'f"""{pre_data_summary}"""')
        with open(f'src/content/{app.config['LANGUAGE']}/results/data_summary.md', 'w') as file:
            file.write(pre_data_summary)

        data_summary = open(f'src/content/{app.config['LANGUAGE']}/results/data_summary.md', 'r').readlines()

        DATA_SUMMARY = {
            'CONTENT': data_summary,
        }

        with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_doc_overview_intro.md', 'r') as file:
            pre_doc_overview_intro = file.read()

        probability_names = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/overview/probability.csv', header = None).iloc[0].tolist()
        # Executive dysfunction probability
        if(EF_RATING == 'VERY LOW'):
            EF_PROBABILITY = probability_names[4] # very likely
        elif(EF_RATING == 'LOW'):
            EF_PROBABILITY = probability_names[3] # likely
        else: # (EF_RATING == 'AVERAGE' or EF_RATING == 'HIGH' or EF_RATING == 'VERY HIGH')
            EF_PROBABILITY = probability_names[2] # possible

        # Medication benefit probability (just looking at inhibition for now)
        if(SAD_RATING == 'VERY LOW'):
            MED_PROBABILITY = probability_names[4] # very likely
        elif(SAD_RATING == 'LOW'):
            MED_PROBABILITY = probability_names[3] # likely
        elif(SAD_RATING == 'AVERAGE'): 
            MED_PROBABILITY = probability_names[2] # possible
        else: # (SAD_RATING == 'HIGH' or SAD_RATING == 'VERY HIGH')
            MED_PROBABILITY = probability_names[1] # unlikely

            # replacing values w/ variables
        pre_doc_overview_intro = eval(f'f"""{pre_doc_overview_intro}"""')
        with open(f'src/content/{app.config['LANGUAGE']}/overview/doc_overview_intro.md', 'w') as file:
            file.write(pre_doc_overview_intro)

        doc_overview_intro = open(f'src/content/{app.config['LANGUAGE']}/overview/doc_overview_intro.md', 'r').readlines()

        DOCTOR_ONLY_CONTENT = {
            'OVERVIEW_INTRO': doc_overview_intro,
        }

        # General Section (Cognitive Profile Summary):
        with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_cog_summary.md', 'r') as file:
            pre_cog_summary = file.read()

        ef_traits = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/overview/EF_trait.csv')
        EF_TRAIT = ef_traits[USER_METRICS['EFCS']['scoreRating']].iloc[0]

        ef_origin_note = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/overview/EF_origin_note.csv')

        # Finding OVERALL strength and weakness
        t_scores = {metric: data['tScore'] for metric, data in USER_METRICS.items()}
        strength = max(t_scores, key=t_scores.get)
        weakness = min(t_scores, key=t_scores.get)

        if(EF_RATING == "LOW" or EF_RATING == "VERY LOW"): # if yes dysfunction, point out weakness
            EF_NOTE = ef_origin_note[ef_origin_note['metricName'] == weakness]['weakness'].iloc[0]
        else: # if no dysfunction, congratulate on strength
            EF_NOTE = ef_origin_note[ef_origin_note['metricName'] == weakness]['strength'].iloc[0]

        STRENGTH = USER_METRICS[strength]['metricLayman']
        WEAKNESS = USER_METRICS[weakness]['metricLayman']

        # CCF Markup
        with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_CCF_markup.md', 'r') as file:
            pre_CCF_markup = file.read()
        if(DIAMOND_CCF != None and STAR_CCF != None):
            CCF_MARKUP = eval(f'f"""{pre_CCF_markup}"""')
        else:
            CCF_MARKUP = ""

        # SCF Markup
        with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_SCF_markup.md', 'r') as file:
            pre_SCF_markup = file.read()
        if(DIAMOND_SCF != None and STAR_SCF != None):
            SCF_MARKUP = eval(f'f"""{pre_SCF_markup}"""')
        else:
            SCF_MARKUP = ""

            # replacing values w/ variables
        pre_cog_summary = eval(f'f"""{pre_cog_summary}"""')
        with open(f'src/content/{app.config['LANGUAGE']}/overview/cog_summary.md', 'w') as file:
            file.write(pre_cog_summary)

        cog_summary = open(f'src/content/{app.config['LANGUAGE']}/overview/cog_summary.md', 'r').readlines()

        OVERVIEW_CONTENT = {
            'COG_SUM': cog_summary,
        }

        ADVICE_INTRO = {}
        path = f'src/content/{app.config['LANGUAGE']}/advice/PersonalizedAdvice.md'
        with open(path, 'r') as file:
            ADVICE_INTRO['INTRO'] = file.readlines()

        ADVICE_DICT = loadAdvice(f'src/content/{app.config['LANGUAGE']}/advice/advice_master.csv')

        # Advice Button Labels
        advice_labels = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/advice/advice_labels.csv', header = None)
        advice_labels = advice_labels.iloc[0].tolist()
        ADVICE_LABELS = {
            'SITUATIONS': {
                'TITLE': advice_labels[6],
                'GETTING_READY': advice_labels[8],
                'ACADEMICS': advice_labels[9],
                'FRIENDS_FAMILY': advice_labels[10],
                'BED': advice_labels[11],
            },
            'STRATEGY': {
                'TITLE': advice_labels[14],
                'EXTERNAL_AID': advice_labels[15],
                'REFRAME': advice_labels[16],
                'RP': advice_labels[17],
                'BA': advice_labels[18],
                'SA': advice_labels[19],
            },
            'N_A': advice_labels[3],
            'LOW': advice_labels[4],
            'HIGH': advice_labels[5],
            'ALL': advice_labels[7],
            'KEEP': advice_labels[12],
            'RESET': advice_labels[20],
            'SHOW': {
                'ALL': advice_labels[1],
                'KEPT': advice_labels[2],
                'BOOKMARK': advice_labels[0],
            },
            'MATCH_LEVEL': {
                'TITLE': advice_labels[13],
            }
        }

        md_paths = {
            'EFCS':f'src/content/{app.config['LANGUAGE']}/about_metrics/EFCS.md', 
            'TACR':f'src/content/{app.config['LANGUAGE']}/about_metrics/TACR.md', 
            'MDS':f'src/content/{app.config['LANGUAGE']}/about_metrics/MDS.md',
            'SAR':f'src/content/{app.config['LANGUAGE']}/about_metrics/SAR.md',
            'SAD':f'src/content/{app.config['LANGUAGE']}/about_metrics/SAD.md',
            'SAV':f'src/content/{app.config['LANGUAGE']}/about_metrics/SAV.md',
        }
        ABOUT_DATA = {}
        for metric, file_path in md_paths.items():
            with open(file_path, 'r') as file:
                ABOUT_DATA[metric] = file.readlines()

        metric_reports = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/metric_report/metric_report.csv', usecols=['metricName','Low','Average','High'])

        METRIC_REPORTS = {
            'EFCS': {
                'REPORT': getReport(USER_METRICS['EFCS']['zScore'], 'EFCS', USER_METRICS['EFCS']['rawValue']),
                'COLOR': getColor(USER_METRICS['EFCS']['zScore']),
            },
            'TACR': {
                'REPORT': getReport(USER_METRICS['TACR']['zScore'], 'TACR', USER_METRICS['TACR']['rawValue']),
                'COLOR': getColor(USER_METRICS['TACR']['zScore']),
            },
            'MDS': {
                'REPORT': getReport(USER_METRICS['MDS']['zScore'], 'MDS', USER_METRICS['MDS']['rawValue']),
                'COLOR': getColor(USER_METRICS['MDS']['zScore']),
            },
            'SAR': {
                'REPORT': getReport(USER_METRICS['SAR']['zScore'], 'SAR', USER_METRICS['SAR']['rawValue']),
                'COLOR': getColor(USER_METRICS['SAR']['zScore']),
            },
            'SAD': {
                'REPORT': getReport(USER_METRICS['SAD']['zScore'], 'SAD', USER_METRICS['SAD']['rawValue']),
                'COLOR': getColor(USER_METRICS['SAD']['zScore']),
            },
            'SAV': {
                'REPORT': getReport(USER_METRICS['SAV']['zScore'], 'SAV', USER_METRICS['SAV']['rawValue']),
                'COLOR': getColor(USER_METRICS['SAV']['zScore']),
            }
        }
        
        return redirect(url_for('index'))
    else:
        return jsonify({
            "error": "Invalid language code. Valid options are ENG, JPN, ESP, FRA."
        }), 400
        
@app.route('/get-UserData', methods=['GET'])
def get_UserData():
    return jsonify(USER_DATA)

# App route
@app.route('/get-HeaderLabels', methods=['GET'])
def get_HeaderLabels():
    return jsonify(HEADERS_LABELS)

def getSymbols(CCF_threshold, SCF_threshold):
    DIAMOND_CCF = None
    STAR_CCF = None
    DIAMOND_SCF = None
    STAR_SCF = None

    # Executive Function
    USER_METRICS['EFCS']['symbol'] = "circle" 

    # Complex Cognitive Functions
    tacr_tScore = USER_METRICS['TACR']['tScore']
    mds_tScore = USER_METRICS['MDS']['tScore']

    if abs(tacr_tScore - mds_tScore) >= CCF_threshold:
        if tacr_tScore > mds_tScore:  # TACR is star (larger)
            USER_METRICS['TACR']['symbol'] = "star" 
            USER_METRICS['MDS']['symbol'] = "diamond" 
            DIAMOND_CCF = MetricInfo[MetricInfo['metricName'] == 'MDS']['laymansName'].iloc[0]
            STAR_CCF = MetricInfo[MetricInfo['metricName'] == 'TACR']['laymansName'].iloc[0]
        else:
            USER_METRICS['TACR']['symbol'] = "diamond" 
            USER_METRICS['MDS']['symbol'] = "star" 
            DIAMOND_CCF = MetricInfo[MetricInfo['metricName'] == 'TACR']['laymansName'].iloc[0]
            STAR_CCF = MetricInfo[MetricInfo['metricName'] == 'MDS']['laymansName'].iloc[0]
    else:
        USER_METRICS['TACR']['symbol'] = "circle" 
        USER_METRICS['MDS']['symbol'] = "circle" 

    # Simpler Cognitive Functions
    sar_tScore = USER_METRICS['SAR']['tScore']
    sad_tScore = USER_METRICS['SAD']['tScore']
    sav_tScore = USER_METRICS['SAV']['tScore']

    tScores = [
        ('SAR', sar_tScore),
        ('SAD', sad_tScore),
        ('SAV', sav_tScore),
    ]
    
    # Find the max and min t-scores
    max_tScore = max(sar_tScore, sad_tScore, sav_tScore)
    min_tScore = min(sar_tScore, sad_tScore, sav_tScore)

    # Check if the difference is at least SCF_threshold
    if (max_tScore - min_tScore) >= SCF_threshold:
        # Sort the list by t-score in descending order
        tScores_sorted = sorted(tScores, key=lambda x: x[1], reverse=True)
        # Assign symbols based on sorted order
        symbols = ['star', 'circle', 'diamond']
        symbol_dict = {metric: symbol for (metric, _), symbol in zip(tScores_sorted, symbols)}
        # Extract the symbols
        USER_METRICS['SAR']['symbol'] = symbol_dict['SAR']
        USER_METRICS['SAD']['symbol'] = symbol_dict['SAD']
        USER_METRICS['SAV']['symbol'] = symbol_dict['SAV'] 

        scf_star_metric = next((metric for metric, symbol in symbol_dict.items() if symbol == 'star'), None)
        scf_diamond_metric = next((metric for metric, symbol in symbol_dict.items() if symbol == 'diamond'), None)

        STAR_SCF = MetricInfo[MetricInfo['metricName'] == scf_star_metric]['laymansName'].iloc[0]
        DIAMOND_SCF = MetricInfo[MetricInfo['metricName'] == scf_diamond_metric]['laymansName'].iloc[0]

    else:
        # Assign all to circle if the difference is less than SCF_threshold
        USER_METRICS['SAR']['symbol'] = "circle"
        USER_METRICS['SAD']['symbol'] = "circle"
        USER_METRICS['SAV']['symbol'] = "circle"

    return DIAMOND_CCF, STAR_CCF, DIAMOND_SCF, STAR_SCF

# Getting Score Ratings
def getScoreRating(zScore):
    if zScore >= 1.5:
        return 'VERY HIGH'
    elif zScore >= 0.5:
        return 'HIGH'
    elif zScore >= -0.5:
        return 'AVERAGE'
    elif zScore >= -1.5:
        return 'LOW'
    else:
        return 'VERY LOW'

# App route
@app.route('/get-UserMetrics', methods=['GET'])
def get_UserMetrics():
    return jsonify(USER_METRICS)

# --------------- RESULTS --------------- #
# Line Chart
def makeLineChart(UserMetrics):
    # Variables
    average_range = 10
    above_avg_color = 'rgba(165, 243, 124, 0.3)'  # Light green
    below_avg_color = 'rgba(243, 224, 124, 0.3)'  # Light yellow
    point_size_circle = 10
    point_size_unique = 16

    # Cap t-scores at 100 and 0 if needed
    # UserMetrics['tScore'] = UserMetrics['tScore'].clip(lower=0, upper=100)
    
    # Define the order of metrics
    metric_names = [f"{USER_METRICS['EFCS']['metricLayman']}<br>(EFCS)",
                    f"{USER_METRICS['TACR']['metricLayman']}<br>(TACR)",
                    f"{USER_METRICS['MDS']['metricLayman']}<br>(MDS)",
                    f"{USER_METRICS['SAD']['metricLayman']}<br>(SAD)",
                    f"{USER_METRICS['SAV']['metricLayman']}<br>(SAV)",
                    f"{USER_METRICS['SAR']['metricLayman']}<br>(SAR)",]
    
    # Create subplots
    fig = make_subplots(rows=1, cols=3, shared_yaxes=False,
                    subplot_titles=(" ", " ", " "),
                    column_widths=[0.2, 0.3, 0.5])

    # Function to get marker symbol and corresponding size
    def get_marker_attributes(metric):
        symbol = USER_METRICS[metric]['symbol']
        size = point_size_circle if symbol == 'circle' else point_size_unique
        return symbol, size

    # Plot Executive Function (EFCS)
    efcs_metric = USER_METRICS["EFCS"]
    efcs_symbol, efcs_size = get_marker_attributes('EFCS')
    fig.add_trace(go.Scatter(
        x=[metric_names[0]],
        y=[efcs_metric['tScore']],
        mode='markers',
        marker=dict(symbol=efcs_symbol, 
                    size=efcs_size, 
                    color='black',
                    opacity=1.0)
    ), row=1, col=1)
    
    # Plot Complex Cognitive Functions
    complex_metrics = {metric: USER_METRICS[metric] for metric in ["TACR", "MDS"] if metric in USER_METRICS}
    complex_symbols_and_sizes = [get_marker_attributes(metric) for metric in complex_metrics.keys()]
    complex_symbols = [attr[0] for attr in complex_symbols_and_sizes]
    complex_sizes = [attr[1] for attr in complex_symbols_and_sizes]
    fig.add_trace(go.Scatter(
        x=metric_names[1:3],
        y=[metrics['tScore'] for metrics in complex_metrics.values() if 'tScore' in metrics],
        mode='lines+markers',
        line=dict(color='black'),
        marker=dict(symbol=complex_symbols,
                    size=complex_sizes,
                    color='black',
                    opacity=1.0)
    ), row=1, col=2)
    
    # Plot Simpler Cognitive Functions
    simple_metrics = {metric: USER_METRICS[metric] for metric in ["SAD", "SAV", "SAR"] if metric in USER_METRICS}
    simple_symbols_and_sizes = [get_marker_attributes(metric) for metric in simple_metrics.keys()]
    simple_symbols = [attr[0] for attr in simple_symbols_and_sizes]
    simple_sizes = [attr[1] for attr in simple_symbols_and_sizes]
    fig.add_trace(go.Scatter(
        x=metric_names[3:],
        y=[metrics['tScore'] for metrics in simple_metrics.values() if 'tScore' in metrics],
        mode='lines+markers',
        line=dict(color='black'),
        marker=dict(symbol=simple_symbols,
                    size=simple_sizes,
                    color='black',
                    opacity=1.0)
    ), row=1, col=3)
    
    # Add colored regions
    for col in [1, 2, 3]:
        fig.add_hrect(y0=50+average_range, y1=100, fillcolor=above_avg_color, line_width=0, row=1, col=col)
        fig.add_hrect(y0=0, y1=50-average_range, fillcolor=below_avg_color, line_width=0, row=1, col=col)
    
    # Update Y-axes
    for col in [1, 2, 3]:
        fig.update_yaxes(
            showline=True, linewidth=1, linecolor='black', title=f"{HEADERS_LABELS['TABLE_LABELS']['T_SCORE']}" if col == 1 else "",
            range=[0, 100], tickmode='array', tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            gridcolor='lightgrey', row=1, col=col,
            showticklabels=True  # Ensure tick labels are shown for all subplots
        )
    
    # Update X-axes
    for col in [1, 2, 3]:
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black', row=1, col=col, tickfont=dict(size=10))
    
    # Update overall layout
    fig.update_layout(
        margin=dict(l=50, r=70, t=80, b=70),  
        title=f"AP-ARC-01 {HEADERS_LABELS['CHART_LABELS']['RESULTS_FOR']} {USER_DATA['USER_NAME']} - {USER_DATA['SESSION_DATE']}",
        showlegend=False,
        plot_bgcolor='white',
        autosize=True
    )

    # Add subplot titles as annotations
    fig.add_annotation(
        x=0.5, y=-0.2,
        xref="x2 domain", yref="paper",
        text=f"{HEADERS_LABELS['METRIC_CATEGORIES']['COMPLEX_COGNITIVE_FUNCTIONS']}",
        showarrow=False,
        font=dict(size=12),
        align="center"
    )

    fig.add_annotation(
        x=0.5, y=-0.2,
        xref="x3 domain", yref="paper",
        text=f"{HEADERS_LABELS['METRIC_CATEGORIES']['SIMPLER_COGNITIVE_FUNCTIONS']}",
        showarrow=False,
        font=dict(size=12),
        align="center"
    )

    fig.add_annotation(
        x=1.1, y=1,
        xref="paper", yref="paper",
        text=f"{HEADERS_LABELS['CHART_LABELS']['LEGEND']}<br>★ {HEADERS_LABELS['CHART_LABELS']['STRENGTH']}<br>◆ {HEADERS_LABELS['CHART_LABELS']['WEAKNESS']}",
        showarrow=False,
        font=dict(size=12),
        align="left",
        bgcolor="white",
        bordercolor="black",
        borderwidth=1
    )
    
    return fig
# App route
@app.route('/get-LineChart', methods=['GET'])
def get_LineChart():
    return jsonify(makeLineChart(UserMetrics=USER_METRICS).to_json())

# Radar Chart
def makeRadarChart(UserMetrics):
    # cap metrics at 3,-3 if needed
    # UserMetrics['zScoreInSample'] = UserMetrics['zScoreInSample'].clip(lower=-3, upper=3)
    
    specific_order = ["EFCS", "TACR", "MDS", "SAR", "SAD", "SAV"]
    # Create the radar chart
    fig = px.line_polar(r=USER_METRICS['zScore'], theta=specific_order, line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
        title="AP-ARC-01 Results for " + str(USER_DATA['USER_NAME']) + " - " + str(USER_DATA['SESSION_DATE']),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[-3, 3]
            )
        ),
        showlegend=False
    )
    return fig
# App route
@app.route('/get-RadarChart', methods=['GET'])
def get_RadarChart():
    return jsonify(makeRadarChart(UserMetrics=USER_METRICS).to_json())

# App route
@app.route('/get-dataSummary', methods=['GET'])
def get_dataSummary():
    return jsonify(DATA_SUMMARY)

# App routes
@app.route('/get-DocOnlyContent', methods=['GET'])
def get_DocOnlyContent():
    return jsonify(DOCTOR_ONLY_CONTENT)
@app.route('/get-OverviewContent', methods=['GET'])
def get_OverviewContent():
    return jsonify(OVERVIEW_CONTENT)
    
def loadAdvice(PATH):
    # GET TAGS
    scen_cols = [
        "Getting Ready",
        "Academics",
        "Friends/Family",
        "Bedtime",
    ]
    strat_cols = [
        "External Aids",
        "Reframing",
        "Role-Playing",
        "Behavior Activation",
        "Successive Approximation",
    ]
    Tags = []
    mr = []
    df = pd.read_csv(PATH)
    for i,r in df.iterrows():
        Tags.append([col for col in scen_cols if r[col] > 0] + [col2 for col2 in strat_cols if r[col2] > 1])
        mr.append(random.randint(1,3))
    df['tags'] = Tags
    df['isKeep'] = 0
    df['Match Level'] = mr
    json_data = df.to_dict(orient='index')
    
    return json_data

# App Routes
@app.route('/get-AdviceIntro', methods=['GET'])
def get_AdviceIntro():
    return jsonify(ADVICE_INTRO)
@app.route('/get-Advice', methods=['GET'])
def get_Advice():
    return jsonify(ADVICE_DICT)
@app.route('/update-Advice', methods=['GET','POST'])
def update_Advice():
    data = request.get_json()
    index = int(data.get('index'))
    keep  = int(data.get('keep'))
    ADVICE_DICT[index]['isKeep'] = keep
    return jsonify(ADVICE_DICT)
@app.route('/get-adviceLabels', methods=['GET'])
def get_adviceLabels():
    return jsonify(ADVICE_LABELS)

# --------------- DOWNLOAD CSV --------------- #
@app.route('/download/UserMetrics', methods=['GET'])
def download_file():
    try:
        # Path to your CSV file
        file_path = f'content/{app.config['LANGUAGE']}/results/{USER_NAME}_UserMetrics.csv'
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get-AboutData', methods=['GET'])
def get_AboutData():
    return jsonify(ABOUT_DATA)

def getReport(zScore, metric, raw_value):
    with open(f'src/content/{app.config['LANGUAGE']}/metric_report/pre_metric_report_scores.md', 'r') as file:
        pre_metric_report_intro = file.read()
    
    NAME = USER_DATA['USER_NAME']
    METRIC = USER_METRICS[metric]['metricLayman']
    METRIC_CODE = metric
    SCORE_RATING = rating_map[USER_METRICS[metric]['scoreRating']]
    METRIC_SCORE = USER_METRICS[metric]['zScore']
    METRIC_AVERAGE = USER_METRICS[metric]['metricAverage']
    ZSCORE = zScore
    METRIC_DESCRIPTION = USER_METRICS[metric]['metricDesc']
    
    if zScore >= 0.5:
        METRIC_REPORT_FROM_TABLE = eval(f'f"""{metric_reports[metric_reports['metricName'] == metric]['High'].iloc[0]}"""')
    elif zScore >= -0.5:
        METRIC_REPORT_FROM_TABLE = eval(f'f"""{metric_reports[metric_reports['metricName'] == metric]['Average'].iloc[0]}"""')
    else:
        METRIC_REPORT_FROM_TABLE = eval(f'f"""{metric_reports[metric_reports['metricName'] == metric]['Low'].iloc[0]}"""')

    pre_metric_report_intro = eval(f'f"""{pre_metric_report_intro}"""')

    with open(rf"src/content/{app.config['LANGUAGE']}/metric_report/generated_reports/metric_report_scores_{metric}.md", 'w') as file:
        file.write(pre_metric_report_intro)
    report = open(rf"src/content/{app.config['LANGUAGE']}/metric_report/generated_reports/metric_report_scores_{metric}.md", 'r').readlines()
    
    return report

# assigning colors for score ratings
def getColor(zScore): 
    if zScore >= 1.5:
        return "#27b335" # Green.
    elif zScore >= 0.5:
        return "#7ec478" # Light Green.
    elif zScore >= -0.5:
        return "#555555" # Grey.
    elif zScore >= -1.5:
        return "#e6c26a" # Light Yellow.
    else:
        return "#d9a118" # Yellow.
    
# Assigning Strengths/Weaknesses (Stars/Diamonds)
CCF_threshold = 10
SCF_threshold = 1

DIAMOND_CCF, STAR_CCF, DIAMOND_SCF, STAR_SCF = getSymbols(CCF_threshold, SCF_threshold)

NAME = USER_DATA['USER_NAME']
ratings = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/ratings.csv', header = None).iloc[0].tolist()
rating_map = {
    'VERY LOW': ratings[0],
    'LOW': ratings[1],
    'AVERAGE': ratings[2],
    'HIGH': ratings[3],
    'VERY HIGH': ratings[4]
}
EF_RAW = USER_METRICS['EFCS']['rawValue']

EF_RATING = rating_map[USER_METRICS['EFCS']['scoreRating']]
TACR_RATING = rating_map[USER_METRICS['TACR']['scoreRating']]
MDS_RATING = rating_map[USER_METRICS['MDS']['scoreRating']]
SAR_RATING = rating_map[USER_METRICS['SAR']['scoreRating']]
SAD_RATING = rating_map[USER_METRICS['SAD']['scoreRating']]
SAV_RATING = rating_map[USER_METRICS['SAV']['scoreRating']]

EF_T_SCORE = USER_METRICS['EFCS']['tScore']
TACR_T_SCORE = USER_METRICS['TACR']['tScore']
MDS_T_SCORE = USER_METRICS['MDS']['tScore']
SAR_T_SCORE = USER_METRICS['SAR']['tScore']
SAD_T_SCORE = USER_METRICS['SAD']['tScore']
SAV_T_SCORE = USER_METRICS['SAV']['tScore']

with open(f'src/content/{app.config['LANGUAGE']}/results/pre_data_summary.md', 'r') as file:
    pre_data_summary = file.read()

relative_results = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/results/relative_results.csv')
print(DIAMOND_CCF, STAR_CCF, DIAMOND_SCF, STAR_SCF)

# CCF
if(DIAMOND_CCF != None and STAR_CCF != None):
    if (EF_RATING == 'LOW' or EF_RATING == 'VERY LOW'):
        CCF_REL = relative_results['low'].iloc[0]
    elif (EF_RATING == 'AVERAGE'):
        CCF_REL = relative_results['average'].iloc[0]
    else: # EF_RATING == 'HIGH' or 'VERY HIGH'
        CCF_REL = relative_results['high'].iloc[0]
else:
    CCF_REL = ""
# SCF
if(DIAMOND_SCF != None and STAR_SCF != None):
    if (EF_RATING == 'LOW' or EF_RATING == 'VERY LOW'):
        SCF_REL = relative_results['low'].iloc[1]
    elif (EF_RATING == 'AVERAGE'):
        SCF_REL = relative_results['average'].iloc[1]
    else: # EF_RATING == 'HIGH' or 'VERY HIGH'
        SCF_REL = relative_results['high'].iloc[1]
else:
    SCF_REL = ""

CCF_RELATIVE = eval(f'f"""{CCF_REL}"""')
SCF_RELATIVE = eval(f'f"""{SCF_REL}"""')
print(CCF_RELATIVE, SCF_RELATIVE)

    # replacing values w/ variables
pre_data_summary = eval(f'f"""{pre_data_summary}"""')
with open(f'src/content/{app.config['LANGUAGE']}/results/data_summary.md', 'w') as file:
    file.write(pre_data_summary)

data_summary = open(f'src/content/{app.config['LANGUAGE']}/results/data_summary.md', 'r').readlines()

DATA_SUMMARY = {
    'CONTENT': data_summary,
}

with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_doc_overview_intro.md', 'r') as file:
    pre_doc_overview_intro = file.read()

probability_names = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/overview/probability.csv', header = None).iloc[0].tolist()
# Executive dysfunction probability
if(EF_RATING == 'VERY LOW'):
    EF_PROBABILITY = probability_names[4] # very likely
elif(EF_RATING == 'LOW'):
    EF_PROBABILITY = probability_names[3] # likely
else: # (EF_RATING == 'AVERAGE' or EF_RATING == 'HIGH' or EF_RATING == 'VERY HIGH')
    EF_PROBABILITY = probability_names[2] # possible

# Medication benefit probability (just looking at inhibition for now)
if(SAD_RATING == 'VERY LOW'):
    MED_PROBABILITY = probability_names[4] # very likely
elif(SAD_RATING == 'LOW'):
    MED_PROBABILITY = probability_names[3] # likely
elif(SAD_RATING == 'AVERAGE'): 
    MED_PROBABILITY = probability_names[2] # possible
else: # (SAD_RATING == 'HIGH' or SAD_RATING == 'VERY HIGH')
    MED_PROBABILITY = probability_names[1] # unlikely

    # replacing values w/ variables
pre_doc_overview_intro = eval(f'f"""{pre_doc_overview_intro}"""')
with open(f'src/content/{app.config['LANGUAGE']}/overview/doc_overview_intro.md', 'w') as file:
    file.write(pre_doc_overview_intro)

doc_overview_intro = open(f'src/content/{app.config['LANGUAGE']}/overview/doc_overview_intro.md', 'r').readlines()

DOCTOR_ONLY_CONTENT = {
    'OVERVIEW_INTRO': doc_overview_intro,
}

# General Section (Cognitive Profile Summary):
with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_cog_summary.md', 'r') as file:
    pre_cog_summary = file.read()

ef_traits = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/overview/EF_trait.csv')
EF_TRAIT = ef_traits[USER_METRICS['EFCS']['scoreRating']].iloc[0]

ef_origin_note = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/overview/EF_origin_note.csv')

# Finding OVERALL strength and weakness
t_scores = {metric: data['tScore'] for metric, data in USER_METRICS.items()}
strength = max(t_scores, key=t_scores.get)
weakness = min(t_scores, key=t_scores.get)

if(EF_RATING == "LOW" or EF_RATING == "VERY LOW"): # if yes dysfunction, point out weakness
    EF_NOTE = ef_origin_note[ef_origin_note['metricName'] == weakness]['weakness'].iloc[0]
else: # if no dysfunction, congratulate on strength
    EF_NOTE = ef_origin_note[ef_origin_note['metricName'] == weakness]['strength'].iloc[0]

STRENGTH = USER_METRICS[strength]['metricLayman']
WEAKNESS = USER_METRICS[weakness]['metricLayman']

# CCF Markup
with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_CCF_markup.md', 'r') as file:
    pre_CCF_markup = file.read()
if(DIAMOND_CCF != None and STAR_CCF != None):
    CCF_MARKUP = eval(f'f"""{pre_CCF_markup}"""')
else:
    CCF_MARKUP = ""

# SCF Markup
with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_SCF_markup.md', 'r') as file:
    pre_SCF_markup = file.read()
if(DIAMOND_SCF != None and STAR_SCF != None):
    SCF_MARKUP = eval(f'f"""{pre_SCF_markup}"""')
else:
    SCF_MARKUP = ""

    # replacing values w/ variables
pre_cog_summary = eval(f'f"""{pre_cog_summary}"""')
with open(f'src/content/{app.config['LANGUAGE']}/overview/cog_summary.md', 'w') as file:
    file.write(pre_cog_summary)

cog_summary = open(f'src/content/{app.config['LANGUAGE']}/overview/cog_summary.md', 'r').readlines()

OVERVIEW_CONTENT = {
    'COG_SUM': cog_summary,
}

ADVICE_INTRO = {}
path = f'src/content/{app.config['LANGUAGE']}/advice/PersonalizedAdvice.md'
with open(path, 'r') as file:
    ADVICE_INTRO['INTRO'] = file.readlines()

ADVICE_DICT = loadAdvice(f'src/content/{app.config['LANGUAGE']}/advice/advice_master.csv')

# Advice Button Labels
advice_labels = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/advice/advice_labels.csv', header = None)
advice_labels = advice_labels.iloc[0].tolist()
ADVICE_LABELS = {
    'SITUATIONS': {
        'TITLE': advice_labels[6],
        'GETTING_READY': advice_labels[8],
        'ACADEMICS': advice_labels[9],
        'FRIENDS_FAMILY': advice_labels[10],
        'BED': advice_labels[11],
    },
    'STRATEGY': {
        'TITLE': advice_labels[14],
        'EXTERNAL_AID': advice_labels[15],
        'REFRAME': advice_labels[16],
        'RP': advice_labels[17],
        'BA': advice_labels[18],
        'SA': advice_labels[19],
    },
    'N_A': advice_labels[3],
    'LOW': advice_labels[4],
    'HIGH': advice_labels[5],
    'ALL': advice_labels[7],
    'KEEP': advice_labels[12],
    'RESET': advice_labels[20],
    'SHOW': {
        'ALL': advice_labels[1],
        'KEPT': advice_labels[2],
        'BOOKMARK': advice_labels[0],
    },
    'MATCH_LEVEL': {
        'TITLE': advice_labels[13],
    }
}

md_paths = {
    'EFCS':f'src/content/{app.config['LANGUAGE']}/about_metrics/EFCS.md', 
    'TACR':f'src/content/{app.config['LANGUAGE']}/about_metrics/TACR.md', 
    'MDS':f'src/content/{app.config['LANGUAGE']}/about_metrics/MDS.md',
    'SAR':f'src/content/{app.config['LANGUAGE']}/about_metrics/SAR.md',
    'SAD':f'src/content/{app.config['LANGUAGE']}/about_metrics/SAD.md',
    'SAV':f'src/content/{app.config['LANGUAGE']}/about_metrics/SAV.md',
}
ABOUT_DATA = {}
for metric, file_path in md_paths.items():
    with open(file_path, 'r') as file:
        ABOUT_DATA[metric] = file.readlines()

metric_reports = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/metric_report/metric_report.csv', usecols=['metricName','Low','Average','High'])

METRIC_REPORTS = {
    'EFCS': {
        'REPORT': getReport(USER_METRICS['EFCS']['zScore'], 'EFCS', USER_METRICS['EFCS']['rawValue']),
        'COLOR': getColor(USER_METRICS['EFCS']['zScore']),
    },
    'TACR': {
        'REPORT': getReport(USER_METRICS['TACR']['zScore'], 'TACR', USER_METRICS['TACR']['rawValue']),
        'COLOR': getColor(USER_METRICS['TACR']['zScore']),
    },
    'MDS': {
        'REPORT': getReport(USER_METRICS['MDS']['zScore'], 'MDS', USER_METRICS['MDS']['rawValue']),
        'COLOR': getColor(USER_METRICS['MDS']['zScore']),
    },
    'SAR': {
        'REPORT': getReport(USER_METRICS['SAR']['zScore'], 'SAR', USER_METRICS['SAR']['rawValue']),
        'COLOR': getColor(USER_METRICS['SAR']['zScore']),
    },
    'SAD': {
        'REPORT': getReport(USER_METRICS['SAD']['zScore'], 'SAD', USER_METRICS['SAD']['rawValue']),
        'COLOR': getColor(USER_METRICS['SAD']['zScore']),
    },
    'SAV': {
        'REPORT': getReport(USER_METRICS['SAV']['zScore'], 'SAV', USER_METRICS['SAV']['rawValue']),
        'COLOR': getColor(USER_METRICS['SAV']['zScore']),
    }
}

# App route
@app.route('/get-MetricReport', methods=['GET'])
def get_MetricReport():
    return jsonify(METRIC_REPORTS)

if __name__ == '__main__':
    app.run(debug=True, port=8000)