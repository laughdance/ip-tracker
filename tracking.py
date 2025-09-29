#!/usr/bin/env python3
import requests, sys, time, random

def slowprint(text, delay=0.02):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def get_ipapi(ip):
    # https://ipapi.co
    try:
        return requests.get(f"https://ipapi.co/{ip}/json/", timeout=10).json()
    except:
        return {}

def get_ipinfo(ip):
    # https://ipinfo.io
    try:
        return requests.get(f"https://ipinfo.io/{ip}/json", timeout=10).json()
    except:
        return {}

def get_ipapicom(ip):
    # https://ip-api.com
    try:
        return requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=10).json()
    except:
        return {}

def get_ipwhois(ip):
    # https://ipwho.is
    try:
        return requests.get(f"http://ipwho.is/{ip}", timeout=10).json()
    except:
        return {}

def get_wikidata_full(country_code):
    try:
        url = "https://query.wikidata.org/sparql"
        query = f"""
        SELECT ?countryLabel ?officialName ?capitalLabel ?currencyLabel ?languageLabel 
               ?population ?area ?callingCode ?flag ?coat ?anthemLabel ?parliamentLabel 
               ?internetDomain ?govFormLabel
               ?headLabel ?dob ?dod ?pobLabel ?podLabel ?partyLabel ?citizenshipLabel 
               ?almaMaterLabel ?occupationLabel ?signature ?website ?photo 
               ?termStart ?termEnd
        WHERE {{
          ?country wdt:P297 "{country_code}".
          OPTIONAL {{ ?country wdt:P1448 ?officialName. }}
          OPTIONAL {{ ?country wdt:P36 ?capital. }}
          OPTIONAL {{ ?country wdt:P38 ?currency. }}
          OPTIONAL {{ ?country wdt:P37 ?language. }}
          OPTIONAL {{ ?country wdt:P1082 ?population. }}
          OPTIONAL {{ ?country wdt:P2046 ?area. }}
          OPTIONAL {{ ?country wdt:P474 ?callingCode. }}
          OPTIONAL {{ ?country wdt:P41 ?flag. }}
          OPTIONAL {{ ?country wdt:P94 ?coat. }}
          OPTIONAL {{ ?country wdt:P85 ?anthem. }}
          OPTIONAL {{ ?country wdt:P194 ?parliament. }}
          OPTIONAL {{ ?country wdt:P78 ?internetDomain. }}
          OPTIONAL {{ ?country wdt:P122 ?govForm. }}

          ?country wdt:P35 ?head.
          OPTIONAL {{ ?head wdt:P569 ?dob. }}
          OPTIONAL {{ ?head wdt:P570 ?dod. }}
          OPTIONAL {{ ?head wdt:P19 ?pob. }}
          OPTIONAL {{ ?head wdt:P20 ?pod. }}
          OPTIONAL {{ ?head wdt:P102 ?party. }}
          OPTIONAL {{ ?head wdt:P27 ?citizenship. }}
          OPTIONAL {{ ?head wdt:P69 ?almaMater. }}
          OPTIONAL {{ ?head wdt:P106 ?occupation. }}
          OPTIONAL {{ ?head wdt:P109 ?signature. }}
          OPTIONAL {{ ?head wdt:P856 ?website. }}
          OPTIONAL {{ ?head wdt:P18 ?photo. }}
          OPTIONAL {{ ?head p:P39 ?pos. ?pos ps:P39 ?office.
                     OPTIONAL {{ ?pos pq:P580 ?termStart. }}
                     OPTIONAL {{ ?pos pq:P582 ?termEnd. }} }}

          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 1
        """
        headers = {"Accept": "application/sparql-results+json"}
        r = requests.get(url, params={"query": query}, headers=headers, timeout=30).json()
        results = r.get("results", {}).get("bindings", [])
        if results:
            res = results[0]
            return {
                "Country (Wikidata)": res.get("countryLabel", {}).get("value", "null"),
                "Official Name": res.get("officialName", {}).get("value", "null"),
                "Capital (Wikidata)": res.get("capitalLabel", {}).get("value", "null"),
                "Currency (Wikidata)": res.get("currencyLabel", {}).get("value", "null"),
                "Language": res.get("languageLabel", {}).get("value", "null"),
                "Population (Wikidata)": res.get("population", {}).get("value", "null"),
                "Area (Wikidata)": res.get("area", {}).get("value", "null"),
                "Calling Code (Wikidata)": res.get("callingCode", {}).get("value", "null"),
                "Flag": res.get("flag", {}).get("value", "null"),
                "Coat of Arms": res.get("coat", {}).get("value", "null"),
                "Anthem": res.get("anthemLabel", {}).get("value", "null"),
                "Parliament": res.get("parliamentLabel", {}).get("value", "null"),
                "Internet Domain": res.get("internetDomain", {}).get("value", "null"),
                "Government Form": res.get("govFormLabel", {}).get("value", "null"),
                "President": res.get("headLabel", {}).get("value", "null"),
                "Date of Birth": res.get("dob", {}).get("value", "null"),
                "Date of Death": res.get("dod", {}).get("value", "null"),
                "Place of Birth": res.get("pobLabel", {}).get("value", "null"),
                "Place of Death": res.get("podLabel", {}).get("value", "null"),
                "Affiliated Parties": res.get("partyLabel", {}).get("value", "null"),
                "Citizenship": res.get("citizenshipLabel", {}).get("value", "null"),
                "Alma Mater": res.get("almaMaterLabel", {}).get("value", "null"),
                "Occupation": res.get("occupationLabel", {}).get("value", "null"),
                "Signature": res.get("signature", {}).get("value", "null"),
                "Website": res.get("website", {}).get("value", "null"),
                "Photo": res.get("photo", {}).get("value", "null"),
                "Term Start": res.get("termStart", {}).get("value", "null"),
                "Term End": res.get("termEnd", {}).get("value", "null"),
            }
    except:
        pass
    return {}

def merge_info(ip):
    d1 = get_ipapi(ip)
    d2 = get_ipinfo(ip)
    d3 = get_ipapicom(ip)
    d4 = get_ipwhois(ip)

    info = {
        "IP Address"    : d1.get("ip") or d2.get("ip") or d3.get("query") or d4.get("ip") or "null",
        "Network"       : d1.get("network") or d4.get("connection", {}).get("domain") or "null",
        "Version"       : d1.get("version") or ("IPv6" if ":" in ip else "IPv4") or "null",
        "City"          : d1.get("city") or d2.get("city") or d3.get("city") or d4.get("city") or "null",
        "Region"        : d1.get("region") or d3.get("regionName") or d4.get("region") or "null",
        "Region Code"   : d1.get("region_code") or d3.get("region") or d4.get("region_code") or "null",
        "Country"       : d1.get("country_name") or d2.get("country") or d3.get("country") or d4.get("country") or "null",
        "Country Code"  : d1.get("country_code") or d3.get("countryCode") or d4.get("country_code") or "null",
        "Continent"     : d1.get("continent") or d3.get("continent") or d4.get("continent") or "null",
        "Continent Code": d1.get("continent_code") or d3.get("continentCode") or d4.get("continent_code") or "null",
        "Capital"       : d1.get("country_capital") or d4.get("country_capital") or "null",
        "Population"    : d1.get("country_population") or d4.get("country_population") or "null",
        "Area (km²)"    : d1.get("country_area") or d4.get("country_area") or "null",
        "Calling Code"  : d1.get("country_calling_code") or d4.get("calling_code") or "null",
        "Postal Code"   : d1.get("postal") or d3.get("zip") or d4.get("postal") or "null",
        "Latitude"      : d1.get("latitude") or (d2.get("loc").split(",")[0] if d2.get("loc") else None) or d3.get("lat") or d4.get("latitude") or "null",
        "Longitude"     : d1.get("longitude") or (d2.get("loc").split(",")[1] if d2.get("loc") else None) or d3.get("lon") or d4.get("longitude") or "null",
        "Timezone"      : d1.get("timezone") or d2.get("timezone") or d3.get("timezone") or d4.get("timezone", {}).get("id") or "null",
        "UTC Offset"    : d1.get("utc_offset") or d3.get("offset") or d4.get("timezone", {}).get("utc") or "null",
        "Languages"     : d1.get("languages") or d4.get("languages") or "null",
        "Currency"      : d1.get("currency") or d4.get("currency") or "null",
        "Currency Name" : d1.get("currency_name") or d4.get("currency_name") or "null",
        "Currency Symbol": d1.get("currency_symbol") or d4.get("currency_symbol") or "null",
        "ASN"           : d1.get("asn") or d3.get("as") or d4.get("connection", {}).get("asn") or "null",
        "ASN Name"      : d3.get("asname") or d4.get("connection", {}).get("org") or "null",
        "Org / ISP"     : d1.get("org") or d2.get("org") or d3.get("isp") or d4.get("connection", {}).get("isp") or "null",
        "Reverse DNS"   : d3.get("reverse") or d4.get("reverse") or "null",
        "Hosting/VPN"   : "Yes" if d3.get("hosting") or d3.get("proxy") or d3.get("mobile") or d4.get("security", {}).get("is_hosting") or d4.get("security", {}).get("is_proxy") else "No",
        "EU Member"     : d1.get("in_eu") or d4.get("is_eu") or "null",
        "Threat Level"  : d4.get("security", {}).get("threat_level") or "null",
        "Mobile"        : d3.get("mobile") or d4.get("security", {}).get("is_mobile") or "No",
        "Proxy"         : d3.get("proxy") or d4.get("security", {}).get("is_proxy") or "No",
        "Tor"           : d4.get("security", {}).get("is_tor") or "No",
    }

    country_code = info.get("Country Code")
    if country_code and country_code != "null":
        wikidata = get_wikidata_full(country_code)
        info.update(wikidata)

    return info

if __name__ == "__main__":
    target = input("Enter target IP (blank=self): ").strip()
    if not target:
        target = requests.get("https://ipapi.co/ip").text.strip()

    slowprint("=== Scanning target... ===", 0.03)
    time.sleep(random.uniform(0.5,1.2))

    info = merge_info(target)

    print("\n=== TARGET INFORMATION REPORT ===")
    for k,v in info.items():
        slowprint(f"{k:25}: {v}", 0.01)

    lat, lon = info.get("Latitude"), info.get("Longitude")
    if lat != "null" and lon != "null":
        map_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=12/{lat}/{lon}"
        slowprint(f"Map Link                 : {map_url}", 0.01)