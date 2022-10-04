from http.client import HTTPResponse
from unicodedata import category
from django.shortcuts import render
import pandas as pd
from lodstorage.sparql import SPARQL
from lodstorage.csv import CSV
import ssl
from .forms import ContactForm

# Create your views here.

def getlink(request):
    ssl._create_default_https_context = ssl._create_unverified_context

    sparqlQuery = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX adms: <http://www.w3.org/ns/adms#>
        PREFIX prov: <http://www.w3.org/ns/prov#>

        SELECT DISTINCT ?ldes FROM <http://stad.gent/ldes/hva> 
        WHERE { 
        ?object adms:identifier ?identifier.
        ?identifier skos:notation ?objectnumber.
        FILTER (regex(?objectnumber, "2004-247-616", "i")).
        ?object prov:generatedAtTime ?time.
        BIND(URI(concat("https://apidg.gent.be/opendata/adlib2eventstream/v1/hva/objecten?generatedAtTime=", ?time)) AS ?ldes)
        } ORDER BY DESC(?object)
        """

    df_sparql = pd.DataFrame()
    sparql = SPARQL("https://stad.gent/sparql")
    qlod = sparql.queryAsListOfDicts(sparqlQuery)
    csv = CSV.toCSV(qlod)
    df_result = pd.DataFrame([x.split(',') for x in csv.split('\n')])
    df_sparql = df_sparql.append(df_result, ignore_index=True)
    table = df_sparql.to_html()
    return render(request, 'ldes.html', {'table': table})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            objectnumber = form.cleaned_data['objectnumber']
            category = form.cleaned_data['category']
            ssl._create_default_https_context = ssl._create_unverified_context

            sparqlQuery = """
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX adms: <http://www.w3.org/ns/adms#>
                PREFIX prov: <http://www.w3.org/ns/prov#>

                SELECT DISTINCT ?ldes FROM <http://stad.gent/ldes/""" + category + """> 
                WHERE { 
                ?object adms:identifier ?identifier.
                ?identifier skos:notation ?objectnumber.
                FILTER (regex(?objectnumber,""" + ' "^' + objectnumber + '$"' + """, "i")).
                ?object prov:generatedAtTime ?time.
                BIND(URI(concat("https://apidg.gent.be/opendata/adlib2eventstream/v1/"""+ category +"""/objecten?generatedAtTime=", ?time)) AS ?ldes)
                } ORDER BY DESC(?object)
                """

            df_sparql = pd.DataFrame()
            sparql = SPARQL("https://stad.gent/sparql")
            qlod = sparql.queryAsListOfDicts(sparqlQuery)
            csv = CSV.toCSV(qlod)
            df_result = pd.DataFrame([x.split(',') for x in csv.split('\n')])
            df_sparql = df_sparql.append(df_result, ignore_index=True)
            df_sparql[0] = df_sparql[0].str.replace(r'"', '')
            ldes = df_sparql[0].iloc[2]
            return render(request, 'ldes.html', {'ldes': ldes})

    form = ContactForm()
    return render(request, 'form.html', {'form':form})