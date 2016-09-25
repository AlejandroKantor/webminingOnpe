#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 3.5
# selenium connects to firefox 47.0.1


"""This script contains the function which are called in getElectionResults"""

# prefixes
# s_ : string
# l_: list
# d_ : dictionary
# df_ : pandas.DataFrame
# sr_ : pandas.Series
#

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np
import re
import time
import sys


def getOptionsHTML( s_html):
    """
    gets the options of a html element
    input: string
    returns: pd.DataFrame
    """

    l_html = s_html.split('\n')
    df_options = pd.DataFrame( l_html, columns= ['source'])

    # keep strings that have the word option
    df_options = df_options[ df_options['source'].str.contains('option')]

    df_options['value'] = df_options['source'].str.replace( '.* value',"")
    df_options['value'] = df_options['value'].str.replace('^="', "")
    df_options['value'] = df_options['value'].str.replace( '".*',"")

    df_options['description'] = df_options['source'].str.replace('.*">', "")
    df_options['description'] = df_options['description'].str.replace('<.*', "")

    df_options.drop('source',1, inplace=True)

    return(df_options)



def getTdValue(s_td, i_pos):
    """
    helper function to get a value from a string with <td> breaks
    input:
        s_td: string with a html <td> breaks
        i_pos: position of <td>s of interest
    output: float value between <td> and </td> of interest coersed to float
    """
    import re
    l_td = s_td.split("</td>")
    s_value = l_td[ i_pos]
    s_value = re.sub('.*>',"",s_value)
    s_value = re.sub('\n', "", s_value)
    s_value = re.sub(',', "", s_value)
    f_value = float(s_value)
    return(f_value)


def getVoteTypeOnpeHTML( s_html):
    """
    input:
        s_html: string with table of number of votes by type of vote
    output: pd.DataFrame of numbe of votes by type of vote
    """

    s_vote_type = re.sub("\n", "", s_html)
    s_vote_type = re.sub("\t", "", s_vote_type)
    l_vote_type  = s_vote_type.split("<tr>")
    l_vote_type = l_vote_type[1:]
    df_vote_type = pd.DataFrame(l_vote_type, columns=['source'])
    df_vote_type['vote_type'] = df_vote_type['source'].str.replace( '</td.*$',"")
    df_vote_type['vote_type'] = df_vote_type['vote_type'].str.replace( '^<td> *',"")

    df_vote_type['votes'] = np.vectorize(getTdValue)(df_vote_type['source'],1)
    df_vote_type['perc_emit'] = np.vectorize(getTdValue)(df_vote_type['source'],3)
    df_vote_type.drop('source',1, inplace=True)
    return( df_vote_type)


def addUbigeoAndLocation(df_obj, s_option,
                         s_amb,
                         s_depart,
                         s_prov,
                         s_dist ):
    """
    Adds to df_obj columns with the values of the other parameters
    input:
        df_obj: pd.DataFrame
        s_option:
        s_amb
        s_depart
        s_prov
        s_dist
    output:
    """

    df_obj['ubigeo'] = s_option
    df_obj['ambito'] = s_amb
    df_obj['departamento'] = s_depart
    df_obj['provincia'] = s_prov
    df_obj['distrito'] = s_dist
    return (df_obj)

def makeResultsDict(wd_obj,
                         elem_obj,
                         df_results,
                         df_vote_type,
                         s_option,
                         s_amb,
                         s_depart='TODOS',
                         s_prov='TODOS',
                         s_dist='TODOS'):

    """
    input:
        s_html
    output:
    """
    d_result = getHtmlStringResults(wd_obj, elem_obj, s_option)
    s_result = d_result['s_result']
    s_vote_type = d_result['s_vote_type']

    df_local_results = getResultsOnpeHTML(s_result)
    df_local_vote_type = getVoteTypeOnpeHTML(s_vote_type)

    df_local_results = addUbigeoAndLocation(df_local_results,s_option, s_amb, s_depart, s_prov, s_dist )
    df_local_vote_type = addUbigeoAndLocation(df_local_vote_type,s_option, s_amb, s_depart, s_prov, s_dist )
    
    df_results = df_results.append(df_local_results, ignore_index=True)
    df_vote_type = df_vote_type.append(df_local_vote_type, ignore_index=True)
    
    d_results = dict(df_results=df_results, df_vote_type= df_vote_type )
    return (d_results)


def getUbigeoStatus(wd_object):
    """
    Gets current ubigeo (geografical code) which is loaded on the page via a wd_object
    input:
        wd_object: web driver object
    output: string with ubigeo code
    """
    eml_ubg_status = wd_object.find_element_by_id('divDetalle')
    s_ubg = eml_ubg_status.get_attribute('innerHTML')
    s_ubg = s_ubg.split("ubigeo=")[1]
    s_ubg = re.sub(re.compile('\\&ambito.*',re.DOTALL),'',s_ubg )
    return(s_ubg)

def getHtmlStringResults(wd_object,elmement , s_option):
    """
    Selects an element in the web driver and then gets strings of vote and type of vote tables
    which is loaded on the page
    input:
        wd_object: web driver object
        element: a web driver element
        s_option: option to be selected in webdriver
    output:
        d_results: dictionary
            ['s_result'] = html string with number of votes table by candidate
            ['s_vote_type'] = html string with number of votes by type
    """
    sel = Select(elmement)

    sel.select_by_value(s_option)

    #check that new option/ubigeo has been updated
    s_ubigeo = getUbigeoStatus(wd_object)

    if s_option != '':
        # if page has not been updated wait til updated for a max time
        count = 0
        while s_option != s_ubigeo and count < 20:
            sel.select_by_value(s_option)
            time.sleep(3)
            s_ubigeo = getUbigeoStatus(wd_object)
            count += 1
            print(count)
            print(s_option)
        if count == 20:
            print( "script stopped because ubigeo would not update\n")
            sys.exit(1)

    eml_result = wd_object.find_element_by_id('page-wrap')
    eml_vote_type = wd_object.find_element_by_class_name('table23' )

    s_result = eml_result.get_attribute('innerHTML')
    s_vote_type = eml_vote_type.get_attribute('innerHTML')
    d_results = dict( s_result = s_result, s_vote_type = s_vote_type)

    return(d_results)

def getResultsOnpeHTML( s_html):
    """gets the options of a html element
    input: string
    returns: pd.DataFrame"""

    l_html = s_html.split('"spaceimg"')
    df_results = pd.DataFrame(l_html, columns=['source'])
    df_results = df_results[df_results['source'].str.contains('height')]

    df_results['party'] = df_results['source'].str.replace('.*px">', "")
    df_results['party'] = df_results['party'].str.replace('<.*', "")

    df_results['party'] = df_results['party'].str.replace('\n', "")
    df_results['party'] = df_results['party'].str.replace('\t', "")

    df_results['temp'] = df_results['source'].str.replace('.*px">', "")

    df_results['votes'] = np.vectorize(getTdValue)(df_results['temp'],1)

    df_results['perc_valid'] = np.vectorize(getTdValue)(df_results['temp'], 2)
    df_results['perc_emit'] = np.vectorize(getTdValue)(df_results['temp'], 3)

    df_results.drop(['source', 'temp'],1, inplace=True )
    return(df_results)



def makeOnpeWebmining( s_url):
    """
    main function of the program
    input: s_url a string with the url from the ONPE agency
    output: d_results a dictionarry with two components
        df_results: pd.DataFrame with the number of votes per candidate per geographical region
        df_vote_type: pd.DataFrame with number of votes by type, valid votes null votes etc by
                            geographical region
    """

    wd_onpe = webdriver.Firefox()
    wd_onpe.get(s_url)


    elm_ambito = wd_onpe.find_element_by_id('cdgoAmbito')
    s_ambito=  elm_ambito.get_attribute('innerHTML')
    df_options = getOptionsHTML(s_ambito)

    #initialize pd.DataFrames

    df_results = pd.DataFrame()
    df_vote_type = pd.DataFrame()

    for index, sr_row in df_options.iterrows():
        s_option = sr_row[ 'value']
        s_amb = sr_row['description']
        print(s_option)
        print(s_amb)

        d_results = makeResultsDict(wd_onpe, elm_ambito, df_results,df_vote_type, s_option, s_amb= s_amb )
        df_results = d_results[ "df_results"]
        df_vote_type = d_results["df_vote_type"]

        elm_dep = wd_onpe.find_element_by_id('cdgoDep')
        s_dep = elm_dep.get_attribute('innerHTML')
        df_options_dep = getOptionsHTML(s_dep)



        if s_option != '':

            for index_dep, sr_row_dep in df_options_dep.iterrows():

                s_option = sr_row_dep['value']
                s_depart = sr_row_dep['description']
                print(s_option)
                print(s_depart)

                d_results = makeResultsDict(wd_onpe, elm_dep, df_results,df_vote_type, s_option,
                                                  s_amb=s_amb, s_depart=s_depart)
                df_results = d_results["df_results"]
                df_vote_type = d_results["df_vote_type"]

                elm_prov = wd_onpe.find_element_by_id('cdgoProv')
                s_prov = elm_prov.get_attribute('innerHTML')
                df_options_prov = getOptionsHTML(s_prov)

                if s_option != '':
                    for index_prov, sr_row_prov in df_options_prov.iterrows():
                        s_option = sr_row_prov['value']
                        s_prov = sr_row_prov['description']
                        print(s_option)
                        print(s_prov)

                        d_results = makeResultsDict(wd_onpe, elm_prov, df_results, df_vote_type,s_option,
                                                          s_amb=s_amb, s_depart=s_depart,
                                                          s_prov = s_prov)
                        df_results = d_results["df_results"]
                        df_vote_type = d_results["df_vote_type"]

                        elm_dist = wd_onpe.find_element_by_id('cdgoDist')
                        s_dist = elm_dist.get_attribute('innerHTML')
                        df_options_dist = getOptionsHTML(s_dist)

                        if s_option != '':

                            for index_dist, sr_row_dist in df_options_dist.iterrows():

                                s_option = sr_row_dist['value']
                                s_dist = sr_row_dist['description']


                                if s_option != '':
                                    print(s_option)
                                    print(s_dist)

                                    d_results = makeResultsDict(wd_onpe, elm_dist, df_results,df_vote_type, s_option,
                                                                      s_amb=s_amb, s_depart=s_depart,
                                                                      s_prov=s_prov,
                                                                      s_dist= s_dist)
                                    df_results = d_results["df_results"]
                                    df_vote_type = d_results["df_vote_type"]
    d_results = dict( df_results=df_results, df_vote_type=df_vote_type)
    return( d_results)


