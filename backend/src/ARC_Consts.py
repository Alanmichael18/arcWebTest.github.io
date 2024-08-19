# response = requests.get('https://xs111291.xsrv.jp/Arc/Data/GetPatientDataForPatientID.php?patientID=' + app.config['USER_NAME'])
# USER_DATA = response.json()
# today = datetime.datetime.today().date()
# birthday = datetime.datetime.strptime(USER_DATA['USER_DOB'], "%Y-%m-%d").date()
# USER_DATA['USER_AGE'] = today.year - birthday.year
# if (today.month, today.day) < (birthday.month, birthday.day):
#         USER_DATA['USER_AGE'] -= 1

# PHP_URL = 'https://xs111291.xsrv.jp/Arc/Data/GetMetricResultsForSession.php?studyID=' + app.config['STUDY_NAME'] + '&sessionID='
# response = requests.get(PHP_URL+app.config['USER_NAME'])
# responseJSON = response.json()
# USER_METRICS = response.json()['results']
# USER_DATA['SESSION_DATE'] = response.json()['SESSION_DATE']

# headers_labels = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/headers_labels.csv')
# HEADERS_LABELS = {
#     'DEMOGRAPHICS': {
#         'DOB': headers_labels['Demographics'].iloc[0],
#         'AGE': headers_labels['Demographics'].iloc[1],
#         'SEX': headers_labels['Demographics'].iloc[2],
#         'SESS_DATE': headers_labels['Demographics'].iloc[3],
#         'SESS_ID': headers_labels['Demographics'].iloc[4],
#         'PLAYER_ID': headers_labels['Demographics'].iloc[5],
#     },
#     'BUTTONS': {
#         'PRINT_REPORT': headers_labels['Buttons'].iloc[0],
#         'ADD_SESSION': headers_labels['Buttons'].iloc[1],
#         'EXPORT_CSV': headers_labels['Buttons'].iloc[2],
#     },
#     'TAB_NAMES': {
#         'OVERVIEW': headers_labels['Tab Names'].iloc[0],
#         'PSYCHOTHERAPY_SUGGESTIONS': headers_labels['Tab Names'].iloc[1],
#         'PERSONALIZED_SUGGESTIONS': headers_labels['Tab Names'].iloc[2],
#         'ABOUT_METRICS': headers_labels['Tab Names'].iloc[3],
#     },
#     'METRIC_CATEGORIES': {
#         'COMPLEX_COGNITIVE_FUNCTIONS': headers_labels['Metric Categories'].iloc[0],
#         'SIMPLER_COGNITIVE_FUNCTIONS': headers_labels['Metric Categories'].iloc[1],
#     },
#     'SECTION_NAMES': {
#         'FOR_DOCTORS': headers_labels['Section Names'].iloc[0],
#         'PERFORMANCE_PLOT': headers_labels['Section Names'].iloc[1],
#         'SCORE_TABLE': headers_labels['Section Names'].iloc[2],
#         'DATA_SUMMARY': headers_labels['Section Names'].iloc[3],
#     },
#     'CHART_LABELS': {
#         'LINE_CHART': headers_labels['Chart Labels'].iloc[0],
#         'RADAR_CHART': headers_labels['Chart Labels'].iloc[1],
#         'RESULTS_FOR': headers_labels['Chart Labels'].iloc[2],
#         'LEGEND': headers_labels['Chart Labels'].iloc[3],
#         'STRENGTH': headers_labels['Chart Labels'].iloc[4],
#         'WEAKNESS': headers_labels['Chart Labels'].iloc[5],
#     },
#     'TABLE_LABELS': {
#         'METRIC': headers_labels['Table Labels'].iloc[0],
#         'FULL_NAME': headers_labels['Table Labels'].iloc[1],
#         'CODE': headers_labels['Table Labels'].iloc[2],
#         'RAW_VALUE': headers_labels['Table Labels'].iloc[3],
#         'AVERAGE': headers_labels['Table Labels'].iloc[4],
#         'T_SCORE': headers_labels['Table Labels'].iloc[5],
#     },
# }

# EXPORT_COLS = ['sessionID', 'metricName', 'metricIdentifier', 'rawValue', 'scoredValue', 'zScoreInSample', 'zScoreInPopulation', 'tScoreInSample', 'tScoreInPopulation', 'metricTitle']
# USER_NAME = USER_DATA['USER_NAME']

# MetricInfo = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/metric_info.csv')
# Averages = pd.read_csv('src/data/Population_Metrics.csv')
# PrimaryMetrics = pd.read_csv('src/data/AllMetrics.csv')
# # UserMetrics = PrimaryMetrics[PrimaryMetrics['sessionID'] == USER_NAME].round(2)
# # UserMetrics[EXPORT_COLS].to_csv(f'src/content/{app.config['LANGUAGE']}/results/{USER_NAME}_UserMetrics.csv')

# metrics = ['EFCS', 'TACR', 'MDS', 'SAD', 'SAR', 'SAV']
# for metric in metrics:
#     USER_METRICS[metric]['rawValue'] = round(USER_METRICS[metric]['rawValue'], 2)
#     USER_METRICS[metric]['zScore'] = round(USER_METRICS[metric]['zScore'], 2)
#     USER_METRICS[metric]['tScore'] = round(USER_METRICS[metric]['tScore'], 2)
#     USER_METRICS[metric]['metricFull'] = MetricInfo[MetricInfo['metricName'] == metric]['fullName'].iloc[0]
#     USER_METRICS[metric]['metricLayman'] = MetricInfo[MetricInfo['metricName'] == metric]['laymansName'].iloc[0]
#     USER_METRICS[metric]['metricDesc'] = MetricInfo[MetricInfo['metricName'] == metric]['description'].iloc[0]
#     USER_METRICS[metric]['metricQuickDesc'] = MetricInfo[MetricInfo['metricName'] == metric]['quickDesc'].iloc[0]
#     USER_METRICS[metric]['metricAverage'] = Averages[Averages['metricName'] == metric]['meanPopulation'].iloc[0]

# # Assigning Strengths/Weaknesses (Stars/Diamonds)
# CCF_threshold = 10
# SCF_threshold = 1

# DIAMOND_CCF, STAR_CCF, DIAMOND_SCF, STAR_SCF = getSymbols(CCF_threshold, SCF_threshold)

# NAME = USER_DATA['USER_NAME']
# ratings = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/ratings.csv', header = None).iloc[0].tolist()
# rating_map = {
#     'VERY LOW': ratings[0],
#     'LOW': ratings[1],
#     'AVERAGE': ratings[2],
#     'HIGH': ratings[3],
#     'VERY HIGH': ratings[4]
# }
# EF_RAW = USER_METRICS['EFCS']['rawValue']

# EF_RATING = rating_map[USER_METRICS['EFCS']['scoreRating']]
# TACR_RATING = rating_map[USER_METRICS['TACR']['scoreRating']]
# MDS_RATING = rating_map[USER_METRICS['MDS']['scoreRating']]
# SAR_RATING = rating_map[USER_METRICS['SAR']['scoreRating']]
# SAD_RATING = rating_map[USER_METRICS['SAD']['scoreRating']]
# SAV_RATING = rating_map[USER_METRICS['SAV']['scoreRating']]

# EF_T_SCORE = USER_METRICS['EFCS']['tScore']
# TACR_T_SCORE = USER_METRICS['TACR']['tScore']
# MDS_T_SCORE = USER_METRICS['MDS']['tScore']
# SAR_T_SCORE = USER_METRICS['SAR']['tScore']
# SAD_T_SCORE = USER_METRICS['SAD']['tScore']
# SAV_T_SCORE = USER_METRICS['SAV']['tScore']

# with open(f'src/content/{app.config['LANGUAGE']}/results/pre_data_summary.md', 'r') as file:
#     pre_data_summary = file.read()

# relative_results = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/results/relative_results.csv')
# print(DIAMOND_CCF, STAR_CCF, DIAMOND_SCF, STAR_SCF)

# # CCF
# if(DIAMOND_CCF != None and STAR_CCF != None):
#     if (EF_RATING == 'LOW' or EF_RATING == 'VERY LOW'):
#         CCF_REL = relative_results['low'].iloc[0]
#     elif (EF_RATING == 'AVERAGE'):
#         CCF_REL = relative_results['average'].iloc[0]
#     else: # EF_RATING == 'HIGH' or 'VERY HIGH'
#         CCF_REL = relative_results['high'].iloc[0]
# else:
#     CCF_REL = ""
# # SCF
# if(DIAMOND_SCF != None and STAR_SCF != None):
#     if (EF_RATING == 'LOW' or EF_RATING == 'VERY LOW'):
#         SCF_REL = relative_results['low'].iloc[1]
#     elif (EF_RATING == 'AVERAGE'):
#         SCF_REL = relative_results['average'].iloc[1]
#     else: # EF_RATING == 'HIGH' or 'VERY HIGH'
#         SCF_REL = relative_results['high'].iloc[1]
# else:
#     SCF_REL = ""

# CCF_RELATIVE = eval(f'f"""{CCF_REL}"""')
# SCF_RELATIVE = eval(f'f"""{SCF_REL}"""')
# print(CCF_RELATIVE, SCF_RELATIVE)

#     # replacing values w/ variables
# pre_data_summary = eval(f'f"""{pre_data_summary}"""')
# with open(f'src/content/{app.config['LANGUAGE']}/results/data_summary.md', 'w') as file:
#     file.write(pre_data_summary)

# data_summary = open(f'src/content/{app.config['LANGUAGE']}/results/data_summary.md', 'r').readlines()

# DATA_SUMMARY = {
#     'CONTENT': data_summary,
# }

# with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_doc_overview_intro.md', 'r') as file:
#     pre_doc_overview_intro = file.read()

# probability_names = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/overview/probability.csv', header = None).iloc[0].tolist()
# # Executive dysfunction probability
# if(EF_RATING == 'VERY LOW'):
#     EF_PROBABILITY = probability_names[4] # very likely
# elif(EF_RATING == 'LOW'):
#     EF_PROBABILITY = probability_names[3] # likely
# else: # (EF_RATING == 'AVERAGE' or EF_RATING == 'HIGH' or EF_RATING == 'VERY HIGH')
#     EF_PROBABILITY = probability_names[2] # possible

# # Medication benefit probability (just looking at inhibition for now)
# if(SAD_RATING == 'VERY LOW'):
#     MED_PROBABILITY = probability_names[4] # very likely
# elif(SAD_RATING == 'LOW'):
#     MED_PROBABILITY = probability_names[3] # likely
# elif(SAD_RATING == 'AVERAGE'): 
#     MED_PROBABILITY = probability_names[2] # possible
# else: # (SAD_RATING == 'HIGH' or SAD_RATING == 'VERY HIGH')
#     MED_PROBABILITY = probability_names[1] # unlikely

#     # replacing values w/ variables
# pre_doc_overview_intro = eval(f'f"""{pre_doc_overview_intro}"""')
# with open(f'src/content/{app.config['LANGUAGE']}/overview/doc_overview_intro.md', 'w') as file:
#     file.write(pre_doc_overview_intro)

# doc_overview_intro = open(f'src/content/{app.config['LANGUAGE']}/overview/doc_overview_intro.md', 'r').readlines()

# DOCTOR_ONLY_CONTENT = {
#     'OVERVIEW_INTRO': doc_overview_intro,
# }

# # General Section (Cognitive Profile Summary):
# with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_cog_summary.md', 'r') as file:
#     pre_cog_summary = file.read()

# ef_traits = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/overview/EF_trait.csv')
# EF_TRAIT = ef_traits[USER_METRICS['EFCS']['scoreRating']].iloc[0]

# ef_origin_note = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/overview/EF_origin_note.csv')

# # Finding OVERALL strength and weakness
# t_scores = {metric: data['tScore'] for metric, data in USER_METRICS.items()}
# strength = max(t_scores, key=t_scores.get)
# weakness = min(t_scores, key=t_scores.get)

# if(EF_RATING == "LOW" or EF_RATING == "VERY LOW"): # if yes dysfunction, point out weakness
#     EF_NOTE = ef_origin_note[ef_origin_note['metricName'] == weakness]['weakness'].iloc[0]
# else: # if no dysfunction, congratulate on strength
#     EF_NOTE = ef_origin_note[ef_origin_note['metricName'] == weakness]['strength'].iloc[0]

# STRENGTH = USER_METRICS[strength]['metricLayman']
# WEAKNESS = USER_METRICS[weakness]['metricLayman']

# # CCF Markup
# with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_CCF_markup.md', 'r') as file:
#     pre_CCF_markup = file.read()
# if(DIAMOND_CCF != None and STAR_CCF != None):
#     CCF_MARKUP = eval(f'f"""{pre_CCF_markup}"""')
# else:
#     CCF_MARKUP = ""

# # SCF Markup
# with open(f'src/content/{app.config['LANGUAGE']}/overview/pre_SCF_markup.md', 'r') as file:
#     pre_SCF_markup = file.read()
# if(DIAMOND_SCF != None and STAR_SCF != None):
#     SCF_MARKUP = eval(f'f"""{pre_SCF_markup}"""')
# else:
#     SCF_MARKUP = ""

#     # replacing values w/ variables
# pre_cog_summary = eval(f'f"""{pre_cog_summary}"""')
# with open(f'src/content/{app.config['LANGUAGE']}/overview/cog_summary.md', 'w') as file:
#     file.write(pre_cog_summary)

# cog_summary = open(f'src/content/{app.config['LANGUAGE']}/overview/cog_summary.md', 'r').readlines()

# OVERVIEW_CONTENT = {
#     'COG_SUM': cog_summary,
# }

# ADVICE_INTRO = {}
# path = f'src/content/{app.config['LANGUAGE']}/advice/PersonalizedAdvice.md'
# with open(path, 'r') as file:
#     ADVICE_INTRO['INTRO'] = file.readlines()

# ADVICE_DICT = loadAdvice(f'src/content/{app.config['LANGUAGE']}/advice/advice_master.csv')

# # Advice Button Labels
# advice_labels = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/advice/advice_labels.csv', header = None)
# advice_labels = advice_labels.iloc[0].tolist()
# ADVICE_LABELS = {
#     'SITUATIONS': {
#         'TITLE': advice_labels[6],
#         'GETTING_READY': advice_labels[8],
#         'ACADEMICS': advice_labels[9],
#         'FRIENDS_FAMILY': advice_labels[10],
#         'BED': advice_labels[11],
#     },
#     'STRATEGY': {
#         'TITLE': advice_labels[14],
#         'EXTERNAL_AID': advice_labels[15],
#         'REFRAME': advice_labels[16],
#         'RP': advice_labels[17],
#         'BA': advice_labels[18],
#         'SA': advice_labels[19],
#     },
#     'N_A': advice_labels[3],
#     'LOW': advice_labels[4],
#     'HIGH': advice_labels[5],
#     'ALL': advice_labels[7],
#     'KEEP': advice_labels[12],
#     'RESET': advice_labels[20],
#     'SHOW': {
#         'ALL': advice_labels[1],
#         'KEPT': advice_labels[2],
#         'BOOKMARK': advice_labels[0],
#     },
#     'MATCH_LEVEL': {
#         'TITLE': advice_labels[13],
#     }
# }

# md_paths = {
#     'EFCS':f'src/content/{app.config['LANGUAGE']}/about_metrics/EFCS.md', 
#     'TACR':f'src/content/{app.config['LANGUAGE']}/about_metrics/TACR.md', 
#     'MDS':f'src/content/{app.config['LANGUAGE']}/about_metrics/MDS.md',
#     'SAR':f'src/content/{app.config['LANGUAGE']}/about_metrics/SAR.md',
#     'SAD':f'src/content/{app.config['LANGUAGE']}/about_metrics/SAD.md',
#     'SAV':f'src/content/{app.config['LANGUAGE']}/about_metrics/SAV.md',
# }
# ABOUT_DATA = {}
# for metric, file_path in md_paths.items():
#     with open(file_path, 'r') as file:
#         ABOUT_DATA[metric] = file.readlines()

# metric_reports = pd.read_csv(f'src/content/{app.config['LANGUAGE']}/metric_report/metric_report.csv', usecols=['metricName','Low','Average','High'])

# METRIC_REPORTS = {
#     'EFCS': {
#         'REPORT': getReport(USER_METRICS['EFCS']['zScore'], 'EFCS', USER_METRICS['EFCS']['rawValue']),
#         'COLOR': getColor(USER_METRICS['EFCS']['zScore']),
#     },
#     'TACR': {
#         'REPORT': getReport(USER_METRICS['TACR']['zScore'], 'TACR', USER_METRICS['TACR']['rawValue']),
#         'COLOR': getColor(USER_METRICS['TACR']['zScore']),
#     },
#     'MDS': {
#         'REPORT': getReport(USER_METRICS['MDS']['zScore'], 'MDS', USER_METRICS['MDS']['rawValue']),
#         'COLOR': getColor(USER_METRICS['MDS']['zScore']),
#     },
#     'SAR': {
#         'REPORT': getReport(USER_METRICS['SAR']['zScore'], 'SAR', USER_METRICS['SAR']['rawValue']),
#         'COLOR': getColor(USER_METRICS['SAR']['zScore']),
#     },
#     'SAD': {
#         'REPORT': getReport(USER_METRICS['SAD']['zScore'], 'SAD', USER_METRICS['SAD']['rawValue']),
#         'COLOR': getColor(USER_METRICS['SAD']['zScore']),
#     },
#     'SAV': {
#         'REPORT': getReport(USER_METRICS['SAV']['zScore'], 'SAV', USER_METRICS['SAV']['rawValue']),
#         'COLOR': getColor(USER_METRICS['SAV']['zScore']),
#     }
# }