import json
import requests
from bs4 import BeautifulSoup 
from PIL import Image
from io import BytesIO
import colorsys
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
from colorthief import ColorThief
import os
import tempfile
import subprocess
import re
import json
import xml.etree.ElementTree as ET 

def hello(event, context):
    # Send an HTTP request to the website's URL to retrieve the HTML source code
    url = event["queryStringParameters"]["website"]
    logo = event["queryStringParameters"]["logo"]
    eventlogo = event["queryStringParameters"]["logo"]
    dominant_color = ""
    font_color = "#fffff"
    # Get a color palette (e.g., for buttons)
    palette = ""
    body = {
      "message": "Function executed failed!",
      "logo": event["queryStringParameters"]["logo"],
      "url": event["queryStringParameters"]["website"],
      "colors": []
    }
    def extract_colors_from_svg_url(svg_url):
        colors = set()

        # Fetch the SVG content from the URL
        response = requests.get(svg_url)
        if response.status_code == 200:
            svg_content = response.text
        else:
            return []

        # Load the SVG content using svgwrite to handle any SVG format
        #root = svgwrite.Drawing()

        # Parse the SVG XML using ElementTree
        root_element = ET.fromstring(svg_content)

        # Function to extract color from an SVG element
        def extract_color(element):
            fill = element.get('fill')
            if fill is not None and fill != 'none':
                colors.add(fill)

        # Iterate through all elements in the SVG
        for element in root_element.iter():
            extract_color(element)

        return list(colors)
    def extract_colors_from_svg(image_url):
        try:
            # Download the SVG image from the URL
            response = requests.get(image_url)
            png_file_path = "/tmp/new"
            if response.status_code == 200:
              # Create a temporary directory
              temp_dir = tempfile.mkdtemp()

              # Generate a unique file name based on the URL
              file_name = os.path.basename(image_url)
              svg_file_path = os.path.join(temp_dir, file_name)
              png_file_path = os.path.join(temp_dir, 'output.png')

              # Download the SVG image from the URL using requests
              response = requests.get(image_url)
              if response.status_code == 200:
                  svg_data = response.content
                  with open(svg_file_path, 'wb') as svg_file:
                      svg_file.write(svg_data)
              else:
                  return {
                      'statusCode': response.status_code,
                      'body': 'Failed to download the image'
                  }

              # Convert SVG to PNG using Inkscape
              subprocess.run(['inkscape', svg_file_path, '--export-filename', png_file_path])

              return png_file_path
            else:
                return None
        except Exception as e:
            print("An error occurred:", str(e))
            return None
    def save_image_from_url_to_temp(image_url):
        try:
            # Download the image from the URL
            response = requests.get(image_url)

            if response.status_code == 200:
                # Create a temporary directory
                temp_dir = tempfile.mkdtemp()

                # Generate a unique file name based on the URL
                file_name = os.path.basename(image_url)
                file_path = os.path.join(temp_dir, file_name)

                # Save the image to the temporary directory
                with open(file_path, 'wb') as file:
                    file.write(response.content)

                # Return the path to the saved image
                return file_path
            else:
                print("Failed to download the image. Status code:", response.status_code)
                return None
        except Exception as e:
            print("An error occurred:", str(e))
            return None
    background_criteria = (0, 0.1, 0.9)  # Background color
    font_criteria = (0, 0.1, 0.9)         # Font color
    border_criteria = (0, 0.1, 0.9)       # Border color
    button_criteria = (0, 0.1, 0.9)      # Button color
    def rgb_to_hex(rgb):
      r, g, b = rgb
      return "#{:02x}{:02x}{:02x}".format(r, g, b)
    all_colors = []
    if (url != ''):
      header = {
         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'
      }
      response = requests.get(url, headers=header)
      # Extract the content of the response
      content = response.content.decode("utf-8")
      soup = BeautifulSoup(content, 'html5lib') 
      if not logo:  # Check if logo is empty
        # Find all <script> tags with type "application/ld+json"
        scripts = soup.find_all("script", type="application/ld+json")
        datax = []
        # Loop through the "@graph" objects to find the logo URL
        for ds in scripts:
          itemx = json.loads(ds.string)
          for item in itemx:
            nex = itemx.get(item, []  )
            if '@type' in nex and nex['@type'] == 'Organization' and 'logo' in nex:
                logo = nex['logo']
                if 'contentUrl' in logo:
                    logo = logo['contentUrl']
                    break  # If we found the logo URL, exit the loop
      if (logo == '') :
        # Find all <a> tags with class containing "logo"
        a_tags = [
            json.loads(x.string) for x in soup.find_all('img', class_=lambda x: x and 'logo' in x) if x.string is not None
        ]
        for a_tag in a_tags:
          if (logo == '') :
            # Find the inner <img> tag
            img_tag = a_tag.find('img')
            if img_tag:
              # Get the src attribute of the inner <img> tag
              logo = img_tag.get('data-src') if img_tag.get('data-src') else img_tag.get('src')
              # If the URL is relative, convert it to an absolute URL
              if not logo.startswith(('http:', 'https:')):
                  logo = urljoin(url, logo)
    if (url != ''):
      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html5lib') 
      if (logo == '') :
        # Define a function to check if "logo" is in the class attribute
        def has_logo_class(class_name):
            return class_name and 'logo' in class_name

        # Find all <a> tags with class containing "logo"
        a_tags = soup.find_all('a', class_=has_logo_class)
        for a_tag in a_tags:
          if (logo == '') :
            # Find the inner <img> tag
            img_tag = a_tag.find('img')
            if img_tag:
              # Get the src attribute of the inner <img> tag
              logo = img_tag.get('data-src') if img_tag.get('data-src') else img_tag.get('src')
              # If the URL is relative, convert it to an absolute URL
              if not logo.startswith(('http:', 'https:')):
                  logo = urljoin(url, logo)
    if (url != ''):
      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html5lib') 
      if (logo == '') :
        # Find all <a> tags with class containing "logo"
        a_tags = soup.find_all('a', class_=lambda x: x and 'brand' in x)
        for a_tag in a_tags:
          if (logo == '') :
            # Find the inner <img> tag
            img_tag = a_tag.find('img')
            if img_tag:
              # Get the src attribute of the inner <img> tag
              logo = img_tag.get('data-src') if img_tag.get('data-src') else img_tag.get('src')
              # If the URL is relative, convert it to an absolute URL
              if not logo.startswith(('http:', 'https:')):
                  logo = urljoin(url, logo)
      if (url != ''):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib') 
        if (logo == '') :
          # Define a function to check if "logo" is in the class attribute
          def has_logo_class(class_name):
              return class_name and 'logo' in class_name

          # Find all <a> tags with class containing "logo"
          a_tags = soup.find_all('a', class_='logo')
          for a_tag in a_tags:
            # Find the inner <img> tag
            img_tag = a_tag.find('img')
            if img_tag:
              # Get the src attribute of the inner <img> tag
              logo = img_tag.get('data-src') if img_tag.get('data-src') else img_tag.get('src')
              # If the URL is relative, convert it to an absolute URL
              if not logo.startswith(('http:', 'https:')):
                  logo = urljoin(url, logo)
      if (logo == '') :
        for img in soup.find_all('img', alt=lambda x: x and ('logo' in x.lower() or 'brand' in x.lower())):
          src = img.get('src')
          if (logo == '') :
            logo = src
            if not logo.startswith(('http:', 'https:')):
                logo = urljoin(url, logo)
          # Find all elements containing the word "logo" in their text
      if (logo == '') :
        # Find all img tags
        img_tags = soup.find_all('img')
        # Iterate through the img tags and check for attributes that indicate it is a logo
        for img_tag in img_tags:
            if img_tag.get('id') == 'logo' or 'logo' in img_tag.get('class', []) or 'custom-logo' in img_tag.get('class', []):
                if (logo == '') :
                  logo = img_tag['src']
                  if not logo.startswith(('http:', 'https:')):
                    logo = urljoin(url, logo)
          # Find all elements containing the word "logo" in their text
      if (logo == '') :
        # Find all <a> tags with class containing "brand"
        a_tags = soup.find_all('a', class_=lambda x: x and ('navbar-brand' in x or 'brand' in x or 'custom-logo' in x or 'logo' in x))
        for a_tag in a_tags:
            # Find the inner <img> tag
            img_tag = a_tag.find('img')
            if img_tag:
              # Get the src attribute of the inner <img> tag
              logo = img_tag.get('data-src') if img_tag.get('data-src') else img_tag.get('src')
              # If the URL is relative, convert it to an absolute URL
              if not logo.startswith(('http:', 'https:')):
                  logo = urljoin(url, logo)

      if (logo == '') :
        # Define a function to filter elements based on class attribute
        def has_brand_class(class_name):
            return class_name and 'brand' in class_name

        # Find elements that have "brand" in their class attribute
        brand_elements = soup.find_all(has_brand_class)
        
        if brand_elements:
            # Iterate through the found elements
            for element in brand_elements:
                # Get the logo's source URL
                logo = element['src']

                # If the URL is relative, convert it to an absolute URL
                if not logo.startswith(('http:', 'https:')):
                    logo = urljoin(url, logo)

      if (logo == ''):
        # Find all <img> elements with class attributes containing 'logo' or 'brand'
        logo_elements = soup.find_all('img', class_=lambda value: value and ('logo' in value.lower() or 'brand' in value.lower()))
        if logo_elements:
          for img_element in logo_elements:
            # Get the logo's source URL
            logo = img_element['src']
            # If the URL is relative, convert it to an absolute URL
            if not logo.startswith(('http:', 'https:')):
                logo = urljoin(url, logo)

      if (logo == '') :
        # Find <a> elements with the "brand" class
        brand_a_tags = soup.find_all('a', class_=lambda value: value and 'brand' in value)
        for a_tag in brand_a_tags:
          # Find the <img> element within the <a> tag
          img_element = a_tag.find('img')
          if img_element:
              # Get the logo's source URL
              logo = img_element['src']
              # If the URL is relative, convert it to an absolute URL
              if not logo.startswith(('http:', 'https:')):
                  logo = urljoin(url, logo)
      if (logo == '' and eventlogo == '') :
          # Replace with your API endpoint and authentication key
          api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiY2Q2YjhlYTQwYjFjOGFmYTJmODRjYjk3Y2Q1ZjZkMzE5MWNjZTFmODFiNGIxYWQ4YzE5MjdjMzQ3YTM5YmQ5OWIwZWQwM2MyMzAxMDkyNzEiLCJpYXQiOjE2OTk0Mjk2NDEuMTU1ODg3LCJuYmYiOjE2OTk0Mjk2NDEuMTU1ODg4LCJleHAiOjE3MzEwNTIwNDEuMTQzNTg4LCJzdWIiOiIxMTQxMiIsInNjb3BlcyI6W119.DkFbvZU2FnqsM8Vnbk0V3g9AvSaeVjJotgZkFAHmdi30UxDAG7bLbm16aFkPGKBFyoJ4GtLrFyOsHPRrSJ54TMBP35gkM47pQTwV5In67GmiQoY6sbrPVEDRRGccKR6h11ecQhjeaAwqS1ebukNXoZeeQvTkHFqzDDLmjQOUF95_ZDEiKJQeS3k4uut2Afb_fvhmQ7-iUxrPyczYIp2P9W4dUPzsH_KvMMBmVN2H6FrSJKyboQy1pITmS7SapukwDXRTFPy9g1Tqr8DYgrA15O7IrVYE8ui_RL0nOhfJktqMsmIQH7-0jFfNnrZtd0LSgAHShSAMv5ENZ1C7pmIMlQ-HNvzzE5EeTEHtSFeR28z70_fej72lptVd6dBQBbtXdWX3faB1Gj7HSGunQwjUTjzW-QoSHdJgbjB9r8WA6Q7rK1BhdY-4IzvKMP_F_2NOz2nKd6RdJWJTNNB5sGA4FUgLs_In3MET0J3PfD9DJHqKUFcZrD8qnEgUghebvK04dJA7M-JYB10jMVrL7SfBtmFCjLu36LxrJDb6IQoqgpjsIG8Kt0KCRfXKwaBUeQV5gtyQlBgVG30cIxxmPIYY9Gs5eJfIW5uBrTpqv10cwbw4rO5JxCTdoFpNywaBgqJxMNmq1VMzg-8Odr83FUZQuH568AspSEutb7rzx7E-ASQ'
          apiurl = "https://www.klazify.com/api/categorize"
          payload = {"url": url}  # Use the dynamically fetched URL
          headers = {
              'Accept': "application/json",
              'Content-Type': "application/json",
              'Authorization': "Bearer "+api_key,  # Replace 'access_key' with your actual access key
              'cache-control': "no-cache"
          }

          # Use the 'json' parameter to send the payload as JSON data
          response = requests.post(apiurl, json=payload, headers=headers)

          if response.status_code == 200:
              # Successful API call
              data = response.json()  # Parse response data (assuming it's in JSON format)
              logo = data['domain']['logo_url']
      if (logo != ''):
        # Send an HTTP request to the URL to get the image content
        response = requests.get(logo)
        if response.status_code == 200:
            if logo.lower().endswith('.svg'):
              # Handle SVG image type
              # You can download or process the SVG as needed
              # Parse the SVG XML content
              svg_xml = response.text

              # Parse the SVG XML using ElementTree
              root = ET.fromstring(svg_xml)

              # Create a set to store unique colors
              colors = set()
              for element in root.iter():
                  if 'stop-color' in element.attrib:
                      color = element.get('stop-color')
                      colors.add(color)
              # Traverse the XML to find colors
              for element in root.iter():
                  if 'fill' in element.attrib:
                      color = element.get('fill')
                      colors.add(color)
              # Find the style element
              style_element = root.find('.//{http://www.w3.org/2000/svg}style')

              # Extract the style text
              if style_element != '':
                style_text = style_element.text if style_element is not None else ''
                if style_text != '':
                  # Split the style text by lines and find the line containing 'stroke:'
                  for line in style_text.split('\n'):
                    if 'stroke:' in line:
                        stroke_property = line.strip()  # Extract the 'stroke' property
                        color_value = stroke_property.split(': ')[1].rstrip(';')
                        colors.add(color_value)
              if colors:
                  for color in colors:
                    if (color != "none" and color != ""):
                      all_colors.append(color)
            else:
              # Read the image content from the response
              image_data = BytesIO(response.content)
              # Open the image using Pillow
              image = Image.open(image_data)
              # Convert the image to RGB mode (if it's not already)
              image = image.convert("RGB")
              # Create a list to store all unique colors
              unique_colors = set()
              # Iterate through the image and collect unique colors
              for pixel in image.getdata():
                unique_colors.add(pixel)
              for color in unique_colors:
                hexcode = rgb_to_hex(color)
                if(len(all_colors) < 20 ):
                  all_colors.append(hexcode)

        if response.status_code == 200:
          if logo.lower().endswith('.svg'):
            temp_file_path = extract_colors_from_svg(logo)
            if (temp_file_path != ''):
            #color_thief = ColorThief(temp_file_path)
              dominant_color = all_colors[0] if len(all_colors) > 0 else '' #color_thief.get_color(quality=1)
              palette = all_colors
              font_color = "#ffffff" if dominant_color == "white" else "#000000"
              """               r, g, b = dominant_color
              luminance = (0.299 * r + 0.587 * g + 0.114 * b)
              font_color = "#ffffff" if luminance < 128 else "#000000"
              dominant_color = rgb_to_hex(dominant_color)
              palette_list = color_thief.get_palette(color_count=3, quality=1)
              palette = []
              for color in palette_list:
                 hexcode = rgb_to_hex(color)
                 palette.append(hexcode)
              # Handle SVG image type
              # You can download or process the SVG as needed
              print("SVG Logo URL:", logo) """
          else:
            # Read the image content from the response
            image_data = BytesIO(response.content)
            # Define criteria for different colors (Hue, Saturation, Lightness ranges)
            # Use ColorThief to extract the dominant color
            temp_file_path = save_image_from_url_to_temp(logo)
            if (temp_file_path != ''):
              color_thief = ColorThief(temp_file_path)
              dominant_color = color_thief.get_color(quality=1)
              r, g, b = dominant_color
              luminance = (0.299 * r + 0.587 * g + 0.114 * b)
              font_color = "#ffffff" if luminance < 128 else "#000000"
              dominant_color = rgb_to_hex(dominant_color)
              palette_list = color_thief.get_palette(color_count=5, quality=1)
              palette = []
              for color in palette_list:
                 hexcode = rgb_to_hex(color)
                 palette.append(hexcode)
            # Iterate through the image and collect colors
      body = {
          "message": "Function executed successfully!",
          "logo": logo,
          "colors": all_colors,
          "background_color": dominant_color,
          "font_color": font_color,
          "button_colors": palette,
          "url": event["queryStringParameters"]["website"]
      }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
