import serial 
import openai
import time
from openai import OpenAI
import pywhatkit

client = OpenAI(api_key="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")

ser = serial.Serial('COM3', 9600, timeout=1) 
time.sleep(2)

def create_summary(temp, hum):
    summary = ask_ai(f"Temperature: {temp}C, Humidity: {hum}%, summary")
    return summary

def  alert(summary):
    phone_number = '+1 548 255 9592'
    pywhatkit.sendwhatmsg_instantly(phone_number, summary, 10, True, 3)

def create_assistant():
    assistant = client.beta.assistants.create(
        name="Humidity Sensor checker",
        instructions= f"""You are an AI that evaluates mold-growth risk, heat-wave danger, indoor-fire risk, hypothermia risk, and dehydration risk using temperature and humidity values from an Arduino (formatted like “25,65”).
Use these formulas:
Mold Growth

Mold Growth Index = ((whichever one is greater, Temperature - 14.001 or 0) divided by (Temperature - 14.001)) x ((whichever one is less, Temperature - 36.001 or 0) divided by (Temperature - 36.001)) x Humidity

No Risk: Mold Growth Index at or under 60

Risk: Mold Growth Index above 60

Heat Wave

Heat Index = Temperature + 0.33 x Humidity - 0.7 - 0.5 x (whichever one is greater, Humidity - 60 or 0)

No Risk: Heat Index at or under 40

Risk: Heat Index over 40

Indoor Fire Risk

Indoor Fire Index = 100 - (Humidity x 1.1) + 0.5 x (whichever one is greater, Temperature - 20 or 0)

No Risk: Indoor Fire Index under 75

Risk: Indoor Fire Index at or over 75

Hypothermia

Hypothermia Index = Temperature - (Humidity x 0.3)

No Risk: Hypothermia Index above -15

Risk: Hypothermia Index at or under -15

Dehydration Risk

Dehydration Index = (whichever one is greater, Temperature - 20 or 0) - (Humidity x 0.2)

No Risk: Dehydration Index under 10

Risk: Dehydration Index at or above 10

Behavior & Output Rules:
Write 6 to 9 sentences, under 35 words total.
Start with: “yes;” or “no;” answering: Are these conditions extremely dangerous?
Then explain:

Whether temp + humidity are normal
Any risks (mold, heat, hypothermia, fire, dehydration).
Te
Short call-to-action if dangerous; if safe, state conditions are normal and you'll notify them if danger appears.

Also analyze humidity patterns:
• Night humidity spikes → poor insulation
• Slow humidity drop post-shower → poor ventilation
• Sudden humidity rise → possible leak

Be professional, polite, concise, and to the point.

""",
        model="gpt-4o"
    )
    
    assistant  = client.beta.assistants.create(
        name="Humidity Sensor Checker",
        instructions='instructions',
        model="gpt-4o"
    )
    return assistant.id

assistant_id = create_assistant()
print("Assistant created with ID:", assistant_id)

def ask_ai(message):
    # Send message
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Wait for completion
    while True:
        status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if status.status == "completed":
            break
        time.sleep(0.3)

    # Get the assistant response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    ai_msg = messages.data[0].content[0].text.value
    return ai_msg

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print("Arduino:", line)

            try:
                temp, hum = map(float, line.split(","))
                print(create_summary(temp,hum))
                ai_response = ask_ai(f"Temperature: {temp}C, Humidity: {hum}%, check for threats at these conditions, such as microbe growth, mold growth and chance of indoor fires and hypothermia, and what can be done to combat these threats in under 50 words")
                # print("\nAI Response:\n", ai_response, "\n")
                # create_summary(temp, hum)
                alert(ai_response)

            except ValueError:
                print("Invalid format from Arduino. Expected 'temp,humidity'.")

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    
finally:
    ser.close()
