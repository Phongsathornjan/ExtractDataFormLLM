# -*- coding: utf-8 -*-

from ollama import chat
from ollama import ChatResponse

from extract_JSON import extract_JSON

try:
  
  print("-------------------Generate Question-------------------")
  response: ChatResponse = chat(model='scb10x/llama3.1-typhoon2-8b-instruct:latest', messages=[
    {
      'role': 'system',
      'content': 'คุณเป็นผู้ใช้งานทั่วไปที่กำลังสนทนากับ chatbot เพื่อถามคำถามเกี่ยวกับการทำอาหารทั้งหมด 3 คำถาม โดยคำถามถัดจากคำถามแรก เป็นการถามต่อเพื่อขยายความจากคำถามก่อนหน้าสั้นๆและกระชับแบบเป็นธรรมชาติ **กฏ** 1. ตอบเป็นภาษาไทยเท่านั้น 2. ตอบกลับมาในรูปแบบ JSON ตามนี้เท่านั้น { "Q1" : "คำถาม", "ANS1" : "คำตอบ", "Q2" : "คำถาม", "ANS2" : "คำตอบ", "Q3" : "คำถาม" }',
    },
  ])

  result = extract_JSON(response['message']['content']) 
  print(result)
  
  print("-------------------Summary Question-------------------")
  response: ChatResponse = chat(model='scb10x/llama3.1-typhoon2-8b-instruct:latest', messages=[
    {
      'role': 'system',
      'content': f'จากข้อมูลบทสนทนาต่อไปนี้ {result} ' + ' คุณคือผู้ช่วยขยายความปรับคำถาม Q3 ให้ชัดเจนขึ้นในคำถามเดียว อ่านแล้วเข้าใจโดยที่ไม่ต้องดูประวัติสนทนาและตอบมาในรูปแบบ JSON ตามนี้ { "output": "ผลลัพธ์" }',
    },
  ])
  
  result = extract_JSON(response['message']['content']) 
  print(result)
    
except Exception as e:
  print(response['message']['content'])
  print(e)
