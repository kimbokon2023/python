import google.generativeai as genai

genai.configure(api_key="AIzaSyDU4BBPxngNjSlI-xdwrIdN0TzWc10_Hyg")

models = genai.list_models()
for m in models:
    print(m.name, ":", m.supported_generation_methods)
