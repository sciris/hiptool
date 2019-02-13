#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 17:09:28 2019

@author: cliffk
"""

import sciris as sc
import hiptool as hp

gbddatafile = 'gbd-data.dat'

def getcountryburden(country):
    # Load data
    try:
        datadir = hp.HPpath('data')
        datafile = sc.loadobj(datadir+gbddatafile)
        countryburden = datafile[country]
    except Exception as E:
        errormsg = 'Could not load data for "%s"; not found as a file or country: %s' % (country, str(E))
        raise Exception(errormsg)
    
    # Error checking -- WARNING, could be improved!
    try:
        burdenkeys = countryburden.keys()
        assert 'DALY'       in burdenkeys[0]
        assert 'Death'      in burdenkeys[1]
        assert 'Prevalence' in burdenkeys[2]
    except Exception as E:
        errormsg = 'Keys DALYs, deaths, and prevalence not in right order: %s (%s)' % (burdenkeys, str(E))
        raise Exception(errormsg)
    return countryburden

countrylist = [
 'Afghanistan',
 'Albania',
 'Algeria',
 'American Samoa',
 'Andorra',
 'Angola',
 'Antigua and Barbuda',
 'Argentina',
 'Armenia',
 'Australia',
 'Austria',
 'Azerbaijan',
 'Bahrain',
 'Bangladesh',
 'Barbados',
 'Belarus',
 'Belgium',
 'Belize',
 'Benin',
 'Bermuda',
 'Bhutan',
 'Bolivia',
 'Bosnia and Herzegovina',
 'Botswana',
 'Brazil',
 'Brunei',
 'Bulgaria',
 'Burkina Faso',
 'Burundi',
 'Cambodia',
 'Cameroon',
 'Canada',
 'Cape Verde',
 'Central African Republic',
 'Chad',
 'Chile',
 'China',
 'Colombia',
 'Comoros',
 'Congo',
 'Costa Rica',
 "Cote d'Ivoire",
 'Croatia',
 'Cuba',
 'Cyprus',
 'Czech Republic',
 'Democratic Republic of the Congo',
 'Denmark',
 'Djibouti',
 'Dominica',
 'Dominican Republic',
 'Ecuador',
 'Egypt',
 'El Salvador',
 'Equatorial Guinea',
 'Eritrea',
 'Estonia',
 'Ethiopia',
 'Federated States of Micronesia',
 'Fiji',
 'Finland',
 'France',
 'Gabon',
 'Georgia',
 'Germany',
 'Ghana',
 'Greece',
 'Greenland',
 'Grenada',
 'Guam',
 'Guatemala',
 'Guinea',
 'Guinea-Bissau',
 'Guyana',
 'Haiti',
 'Honduras',
 'Hungary',
 'Iceland',
 'India',
 'Indonesia',
 'Iran',
 'Iraq',
 'Ireland',
 'Israel',
 'Italy',
 'Jamaica',
 'Japan',
 'Jordan',
 'Kazakhstan',
 'Kenya',
 'Kiribati',
 'Kuwait',
 'Kyrgyzstan',
 'Laos',
 'Latvia',
 'Lebanon',
 'Lesotho',
 'Liberia',
 'Libya',
 'Lithuania',
 'Luxembourg',
 'Macedonia',
 'Madagascar',
 'Malawi',
 'Malaysia',
 'Maldives',
 'Mali',
 'Malta',
 'Marshall Islands',
 'Mauritania',
 'Mauritius',
 'Mexico',
 'Moldova',
 'Mongolia',
 'Montenegro',
 'Morocco',
 'Mozambique',
 'Myanmar',
 'Namibia',
 'Nepal',
 'Netherlands',
 'New Zealand',
 'Nicaragua',
 'Niger',
 'Nigeria',
 'North Korea',
 'Northern Mariana Islands',
 'Norway',
 'Oman',
 'Pakistan',
 'Palestine',
 'Panama',
 'Papua New Guinea',
 'Paraguay',
 'Peru',
 'Philippines',
 'Poland',
 'Portugal',
 'Puerto Rico',
 'Qatar',
 'Romania',
 'Russian Federation',
 'Rwanda',
 'Saint Lucia',
 'Saint Vincent and the Grenadines',
 'Samoa',
 'Sao Tome and Principe',
 'Saudi Arabia',
 'Senegal',
 'Serbia',
 'Seychelles',
 'Sierra Leone',
 'Singapore',
 'Slovakia',
 'Slovenia',
 'Solomon Islands',
 'Somalia',
 'South Africa',
 'South Korea',
 'South Sudan',
 'Spain',
 'Sri Lanka',
 'Sudan',
 'Suriname',
 'Swaziland',
 'Sweden',
 'Switzerland',
 'Syria',
 'Taiwan',
 'Tajikistan',
 'Tanzania',
 'Thailand',
 'The Bahamas',
 'The Gambia',
 'Timor-Leste',
 'Togo',
 'Tonga',
 'Trinidad and Tobago',
 'Tunisia',
 'Turkey',
 'Turkmenistan',
 'Uganda',
 'Ukraine',
 'United Arab Emirates',
 'United Kingdom',
 'United States',
 'Uruguay',
 'Uzbekistan',
 'Vanuatu',
 'Venezuela',
 'Vietnam',
 'Virgin Islands, U.S.',
 'Yemen',
 'Zambia',
 'Zimbabwe',
]

causedict = sc.odict([
("Acne vulgaris", "B.9.7"),
("Acute glomerulonephritis", "B.8.3"),
("Acute hepatitis", "A.5.8"),
("Acute hepatitis A", "A.5.8.1"),
("Acute hepatitis B", "A.5.8.2"),
("Acute hepatitis C", "A.5.8.3"),
("Acute hepatitis E", "A.5.8.4"),
("Acute lymphoid leukemia", "B.1.28.1"),
("Acute myeloid leukemia", "B.1.28.3"),
("Adverse effects of medical treatment", "C.2.6"),
("African trypanosomiasis", "A.4.4"),
("Age-related and other hearing loss", "B.10.2"),
("Age-related macular degeneration", "B.10.1.3"),
("Alcohol use disorders", "B.7.1"),
("Alcoholic cardiomyopathy", "B.2.6.2"),
("All causes", "T"),
("Alopecia areata", "B.9.8"),
("Alzheimer's disease and other dementias", "B.5.1"),
("Amphetamine use disorders", "B.7.2.3"),
("Animal contact", "C.2.7"),
("Anorexia nervosa", "B.6.5.1"),
("Anxiety disorders", "B.6.4"),
("Aortic aneurysm", "B.2.8"),
("Appendicitis", "B.4.3"),
("Asbestosis", "B.3.2.2"),
("Ascariasis", "A.4.14.1"),
("Asthma", "B.3.3"),
("Atopic dermatitis", "B.9.1.1"),
("Atrial fibrillation and flutter", "B.2.7"),
("Attention-deficit/hyperactivity disorder", "B.6.7"),
("Autism spectrum disorders", "B.6.6"),
("Bacterial skin diseases", "B.9.3"),
("Benign and in situ cervical and uterine neoplasms", "B.1.30.3"),
("Benign and in situ intestinal neoplasms", "B.1.30.2"),
("Benign prostatic hyperplasia", "B.12.2.3"),
("Bipolar disorder", "B.6.3"),
("Bladder cancer", "B.1.21"),
("Blindness and vision impairment", "B.10.1"),
("Brain and nervous system cancer", "B.1.22"),
("Breast cancer", "B.1.14"),
("Bulimia nervosa", "B.6.5.2"),
("Cannabis use disorders", "B.7.2.4"),
("Cardiomyopathy and myocarditis", "B.2.6"),
("Cardiovascular diseases", "B.2"),
("Caries of deciduous teeth", "B.12.6.1"),
("Caries of permanent teeth", "B.12.6.2"),
("Cataract", "B.10.1.2"),
("Cellulitis", "B.9.3.1"),
("Cervical cancer", "B.1.15"),
("Chagas disease", "A.4.2"),
("Chlamydial infection", "A.1.2.2"),
("Chronic kidney disease", "B.8.2"),
("Chronic kidney disease due to diabetes mellitus type 1", "B.8.2.1"),
("Chronic kidney disease due to diabetes mellitus type 2", "B.8.2.2"),
("Chronic kidney disease due to glomerulonephritis", "B.8.2.4"),
("Chronic kidney disease due to hypertension", "B.8.2.3"),
("Chronic kidney disease due to other and unspecified causes", "B.8.2.5"),
("Chronic lymphoid leukemia", "B.1.28.2"),
("Chronic myeloid leukemia", "B.1.28.4"),
("Chronic obstructive pulmonary disease", "B.3.1"),
("Chronic respiratory diseases", "B.3"),
("Cirrhosis and other chronic liver diseases", "B.4.1"),
("Cirrhosis and other chronic liver diseases due to alcohol use", "B.4.1.3"),
("Cirrhosis and other chronic liver diseases due to hepatitis B", "B.4.1.1"),
("Cirrhosis and other chronic liver diseases due to hepatitis C", "B.4.1.2"),
("Cirrhosis and other chronic liver diseases due to other causes", "B.4.1.5"),
("Cirrhosis due to NASH", "B.4.1.4"),
("Coal workers pneumoconiosis", "B.3.2.3"),
("Cocaine use disorders", "B.7.2.2"),
("Colon and rectum cancer", "B.1.6"),
("Communicable, maternal, neonatal, and nutritional diseases", "A"),
("Conduct disorder", "B.6.8"),
("Conflict and terrorism", "C.3.3"),
("Congenital birth defects", "B.12.1"),
("Congenital heart anomalies", "B.12.1.2"),
("Congenital musculoskeletal and limb anomalies", "B.12.1.8"),
("Contact dermatitis", "B.9.1.2"),
("Cutaneous and mucocutaneous leishmaniasis", "A.4.3.2"),
("Cyclist road injuries", "C.1.1.2"),
("Cystic echinococcosis", "A.4.7"),
("Cysticercosis", "A.4.6"),
("Decubitus ulcer", "B.9.11"),
("Dengue", "A.4.11"),
("Depressive disorders", "B.6.2"),
("Dermatitis", "B.9.1"),
("Diabetes and kidney diseases", "B.8"),
("Diabetes mellitus", "B.8.1"),
("Diabetes mellitus type 1", "B.8.1.1"),
("Diabetes mellitus type 2", "B.8.1.2"),
("Diarrheal diseases", "A.3.1"),
("Dietary iron deficiency", "A.7.4"),
("Digestive congenital anomalies", "B.12.1.10"),
("Digestive diseases", "B.4"),
("Diphtheria", "A.5.3"),
("Down syndrome", "B.12.1.4"),
("Drowning", "C.2.2"),
("Drug use disorders", "B.7.2"),
("Drug-susceptible tuberculosis", "A.2.1.2"),
("Dysthymia", "B.6.2.2"),
("Eating disorders", "B.6.5"),
("Ebola", "A.4.17"),
("Ectopic pregnancy", "A.6.1.6"),
("Edentulism and severe tooth loss", "B.12.6.4"),
("Encephalitis", "A.5.2"),
("Endocarditis", "B.2.10"),
("Endocrine, metabolic, blood, and immune disorders", "B.12.5"),
("Endometriosis", "B.12.3.4"),
("Enteric infections", "A.3"),
("Environmental heat and cold exposure", "C.2.9"),
("Epilepsy", "B.5.3"),
("Esophageal cancer", "B.1.4"),
("Executions and police conflict", "C.3.4"),
("Exposure to forces of nature", "C.2.10"),
("Exposure to mechanical forces", "C.2.5"),
("Extensively drug-resistant tuberculosis", "A.2.1.4"),
("Falls", "C.2.1"),
("Female infertility", "B.12.3.3"),
("Fire, heat, and hot substances", "C.2.3"),
("Food-borne trematodiases", "A.4.15"),
("Foreign body", "C.2.8"),
("Foreign body in eyes", "C.2.8.2"),
("Foreign body in other body part", "C.2.8.3"),
("Fungal skin diseases", "B.9.5"),
("G6PD deficiency", "B.12.4.5"),
("G6PD trait", "B.12.4.6"),
("Gallbladder and biliary diseases", "B.4.8"),
("Gallbladder and biliary tract cancer", "B.1.8"),
("Gastritis and duodenitis", "B.4.2.2"),
("Gastroesophageal reflux disease", "B.4.2.3"),
("Genital herpes", "A.1.2.5"),
("Genital prolapse", "B.12.3.5"),
("Glaucoma", "B.10.1.1"),
("Gonococcal infection", "A.1.2.3"),
("Gout", "B.11.5"),
("Guinea worm disease", "A.4.19"),
("Gynecological diseases", "B.12.3"),
("H influenzae type B meningitis", "A.5.1.2"),
("Headache disorders", "B.5.6"),
("Hemoglobinopathies and hemolytic anemias", "B.12.4"),
("Hemolytic disease and other neonatal jaundice", "A.6.2.4"),
("HIV/AIDS", "A.1.1"),
("HIV/AIDS - Drug-susceptible Tuberculosis", "A.1.1.1"),
("HIV/AIDS - Extensively drug-resistant Tuberculosis", "A.1.1.3"),
("HIV/AIDS - Multidrug-resistant Tuberculosis without extensive drug resistance", "A.1.1.2"),
("HIV/AIDS and sexually transmitted infections", "A.1"),
("HIV/AIDS resulting in other diseases", "A.1.1.4"),
("Hodgkin lymphoma", "B.1.25"),
("Hookworm disease", "A.4.14.3"),
("Hypertensive heart disease", "B.2.4"),
("Idiopathic developmental intellectual disability", "B.6.9"),
("Indirect maternal deaths", "A.6.1.7"),
("Inflammatory bowel disease", "B.4.6"),
("Inguinal, femoral, and abdominal hernia", "B.4.5"),
("Injuries", "C"),
("Interpersonal violence", "C.3.2"),
("Interstitial lung disease and pulmonary sarcoidosis", "B.3.4"),
("Intestinal nematode infections", "A.4.14"),
("Intracerebral hemorrhage", "B.2.3.2"),
("Invasive Non-typhoidal Salmonella (iNTS)", "A.3.3"),
("Iodine deficiency", "A.7.2"),
("Ischemic heart disease", "B.2.2"),
("Ischemic stroke", "B.2.3.1"),
("Kidney cancer", "B.1.20"),
("Klinefelter syndrome", "B.12.1.6"),
("Larynx cancer", "B.1.10"),
("Late maternal deaths", "A.6.1.8"),
("Latent tuberculosis infection", "A.2.1.1"),
("Leishmaniasis", "A.4.3"),
("Leprosy", "A.4.16"),
("Leukemia", "B.1.28"),
("Lip and oral cavity cancer", "B.1.1"),
("Liver cancer", "B.1.7"),
("Liver cancer due to alcohol use", "B.1.7.3"),
("Liver cancer due to hepatitis B", "B.1.7.1"),
("Liver cancer due to hepatitis C", "B.1.7.2"),
("Liver cancer due to NASH", "B.1.7.4"),
("Liver cancer due to other causes", "B.1.7.5"),
("Low back pain", "B.11.3"),
("Lower respiratory infections", "A.2.2"),
("Lymphatic filariasis", "A.4.8"),
("Major depressive disorder", "B.6.2.1"),
("Malaria", "A.4.1"),
("Male infertility", "B.12.2.4"),
("Malignant skin melanoma", "B.1.12"),
("Maternal abortion and miscarriage", "A.6.1.5"),
("Maternal and neonatal disorders", "A.6"),
("Maternal deaths aggravated by HIV/AIDS", "A.6.1.9"),
("Maternal disorders", "A.6.1"),
("Maternal hemorrhage", "A.6.1.1"),
("Maternal hypertensive disorders", "A.6.1.3"),
("Maternal obstructed labor and uterine rupture", "A.6.1.4"),
("Maternal sepsis and other maternal infections", "A.6.1.2"),
("Measles", "A.5.6"),
("Meningitis", "A.5.1"),
("Meningococcal meningitis", "A.5.1.3"),
("Mental disorders", "B.6"),
("Mesothelioma", "B.1.24"),
("Migraine", "B.5.6.1"),
("Motor neuron disease", "B.5.5"),
("Motor vehicle road injuries", "C.1.1.4"),
("Motorcyclist road injuries", "C.1.1.3"),
("Multidrug-resistant tuberculosis without extensive drug resistance", "A.2.1.3"),
("Multiple myeloma", "B.1.27"),
("Multiple sclerosis", "B.5.4"),
("Musculoskeletal disorders", "B.11"),
("Myelodysplastic, myeloproliferative, and other hematopoietic neoplasms", "B.1.30.1"),
("Myocarditis", "B.2.6.1"),
("Nasopharynx cancer", "B.1.2"),
("Near vision loss", "B.10.1.5"),
("Neck pain", "B.11.4"),
("Neglected tropical diseases and malaria", "A.4"),
("Neonatal disorders", "A.6.2"),
("Neonatal encephalopathy due to birth asphyxia and trauma", "A.6.2.2"),
("Neonatal preterm birth", "A.6.2.1"),
("Neonatal sepsis and other neonatal infections", "A.6.2.3"),
("Neoplasms", "B.1"),
("Neural tube defects", "B.12.1.1"),
("Neurological disorders", "B.5"),
("Non-communicable diseases", "B"),
("Non-Hodgkin lymphoma", "B.1.26"),
("Non-melanoma skin cancer", "B.1.13"),
("Non-melanoma skin cancer (basal-cell carcinoma)", "B.1.13.2"),
("Non-melanoma skin cancer (squamous-cell carcinoma)", "B.1.13.1"),
("Non-rheumatic calcific aortic valve disease", "B.2.5.1"),
("Non-rheumatic degenerative mitral valve disease", "B.2.5.2"),
("Non-rheumatic valvular heart disease", "B.2.5"),
("Non-venomous animal contact", "C.2.7.2"),
("Nutritional deficiencies", "A.7"),
("Onchocerciasis", "A.4.9"),
("Opioid use disorders", "B.7.2.1"),
("Oral disorders", "B.12.6"),
("Orofacial clefts", "B.12.1.3"),
("Osteoarthritis", "B.11.2"),
("Other benign and in situ neoplasms", "B.1.30.4"),
("Other cardiomyopathy", "B.2.6.3"),
("Other cardiovascular and circulatory diseases", "B.2.11"),
("Other chromosomal abnormalities", "B.12.1.7"),
("Other chronic respiratory diseases", "B.3.5"),
("Other congenital birth defects", "B.12.1.11"),
("Other digestive diseases", "B.4.10"),
("Other drug use disorders", "B.7.2.5"),
("Other exposure to mechanical forces", "C.2.5.2"),
("Other gynecological diseases", "B.12.3.7"),
("Other hemoglobinopathies and hemolytic anemias", "B.12.4.7"),
("Other infectious diseases", "A.5"),
("Other intestinal infectious diseases", "A.3.4"),
("Other leukemia", "B.1.28.5"),
("Other malignant neoplasms", "B.1.29"),
("Other maternal disorders", "A.6.1.10"),
("Other meningitis", "A.5.1.4"),
("Other mental disorders", "B.6.10"),
("Other musculoskeletal disorders", "B.11.6"),
("Other neglected tropical diseases", "A.4.20"),
("Other neonatal disorders", "A.6.2.5"),
("Other neoplasms", "B.1.30"),
("Other neurological disorders", "B.5.7"),
("Other non-communicable diseases", "B.12"),
("Other non-rheumatic valve diseases", "B.2.5.3"),
("Other nutritional deficiencies", "A.7.5"),
("Other oral disorders", "B.12.6.5"),
("Other pharynx cancer", "B.1.3"),
("Other pneumoconiosis", "B.3.2.4"),
("Other road injuries", "C.1.1.5"),
("Other sense organ diseases", "B.10.3"),
("Other sexually transmitted infections", "A.1.2.6"),
("Other skin and subcutaneous diseases", "B.9.12"),
("Other transport injuries", "C.1.2"),
("Other unintentional injuries", "C.2.11"),
("Other unspecified infectious diseases", "A.5.9"),
("Other urinary diseases", "B.12.2.5"),
("Other vision loss", "B.10.1.6"),
("Otitis media", "A.2.4"),
("Ovarian cancer", "B.1.17"),
("Pancreatic cancer", "B.1.9"),
("Pancreatitis", "B.4.9"),
("Paralytic ileus and intestinal obstruction", "B.4.4"),
("Paratyphoid fever", "A.3.2.2"),
("Parkinson's disease", "B.5.2"),
("Pedestrian road injuries", "C.1.1.1"),
("Peptic ulcer disease", "B.4.2.1"),
("Periodontal diseases", "B.12.6.3"),
("Peripheral artery disease", "B.2.9"),
("Physical violence by firearm", "C.3.2.1"),
("Physical violence by other means", "C.3.2.4"),
("Physical violence by sharp object", "C.3.2.2"),
("Pneumococcal meningitis", "A.5.1.1"),
("Pneumoconiosis", "B.3.2"),
("Poisoning by carbon monoxide", "C.2.4.1"),
("Poisoning by other means", "C.2.4.2"),
("Poisonings", "C.2.4"),
("Polycystic ovarian syndrome", "B.12.3.2"),
("Premenstrual syndrome", "B.12.3.6"),
("Prostate cancer", "B.1.18"),
("Protein-energy malnutrition", "A.7.1"),
("Pruritus", "B.9.9"),
("Psoriasis", "B.9.2"),
("Pulmonary aspiration and foreign body in airway", "C.2.8.1"),
("Pyoderma", "B.9.3.2"),
("Rabies", "A.4.13"),
("Refraction disorders", "B.10.1.4"),
("Respiratory infections and tuberculosis", "A.2"),
("Rheumatic heart disease", "B.2.1"),
("Rheumatoid arthritis", "B.11.1"),
("Road injuries", "C.1.1"),
("Scabies", "B.9.4"),
("Schistosomiasis", "A.4.5"),
("Schizophrenia", "B.6.1"),
("Seborrhoeic dermatitis", "B.9.1.3"),
("Self-harm", "C.3.1"),
("Self-harm and interpersonal violence", "C.3"),
("Self-harm by firearm", "C.3.1.1"),
("Self-harm by other specified means", "C.3.1.2"),
("Sense organ diseases", "B.10"),
("Sexual violence", "C.3.2.3"),
("Sexually transmitted infections excluding HIV", "A.1.2"),
("Sickle cell disorders", "B.12.4.3"),
("Sickle cell trait", "B.12.4.4"),
("Silicosis", "B.3.2.1"),
("Skin and subcutaneous diseases", "B.9"),
("Stomach cancer", "B.1.5"),
("Stroke", "B.2.3"),
("Subarachnoid hemorrhage", "B.2.3.3"),
("Substance use disorders", "B.7"),
("Sudden infant death syndrome", "B.12.7"),
("Syphilis", "A.1.2.1"),
("Tension-type headache", "B.5.6.2"),
("Testicular cancer", "B.1.19"),
("Tetanus", "A.5.5"),
("Thalassemias", "B.12.4.1"),
("Thalassemias trait", "B.12.4.2"),
("Thyroid cancer", "B.1.23"),
("Tracheal, bronchus, and lung cancer", "B.1.11"),
("Trachoma", "A.4.10"),
("Transport injuries", "C.1"),
("Trichomoniasis", "A.1.2.4"),
("Trichuriasis", "A.4.14.2"),
("Tuberculosis", "A.2.1"),
("Turner syndrome", "B.12.1.5"),
("Typhoid and paratyphoid", "A.3.2"),
("Typhoid fever", "A.3.2.1"),
("Unintentional firearm injuries", "C.2.5.1"),
("Unintentional injuries", "C.2"),
("Upper digestive system diseases", "B.4.2"),
("Upper respiratory infections", "A.2.3"),
("Urinary diseases and male infertility", "B.12.2"),
("Urinary tract infections", "B.12.2.1"),
("Urogenital congenital anomalies", "B.12.1.9"),
("Urolithiasis", "B.12.2.2"),
("Urticaria", "B.9.10"),
("Uterine cancer", "B.1.16"),
("Uterine fibroids", "B.12.3.1"),
("Varicella and herpes zoster", "A.5.7"),
("Vascular intestinal disorders", "B.4.7"),
("Venomous animal contact", "C.2.7.1"),
("Viral skin diseases", "B.9.6"),
("Visceral leishmaniasis", "A.4.3.1"),
("Vitamin A deficiency", "A.7.3"),
("Whooping cough", "A.5.4"),
("Yellow fever", "A.4.12"),
("Zika virus", "A.4.18"),
        ])

codes = causedict.values()
sorco = sorted(codes)
codestring = '\n'.join(sorco)
twigcausedict = sc.odict()
for co in sorco:
    twigcausedict[co] = codestring.count(co)==1 and co!='T'