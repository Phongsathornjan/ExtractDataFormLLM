# -*- coding: utf-8 -*-
import time
from ollama import chat
from ollama import ChatResponse

from extract_JSON import extract_JSON

try:
  
  
  start_time1 = time.time()
  print("-------------------Generate Question-------------------")
  response: ChatResponse = chat(model='scb10x/llama3.1-typhoon2-8b-instruct:latest', messages=[
    {
      'role': 'system',
      'content': 'คุณเป็นผู้ใช้งานทั่วไปที่กำลังสนทนากับ chatbot เพื่อถามคำถามทั่วไปทั้งหมด 3 คำถามสั้นๆ โดยคำถามถัดจากคำถามแรก เป็นการถามต่อเพื่อขยายความจากคำถามก่อนหน้าสั้นๆ กระชับ และเป็นธรรมชาติ **กฏ** 1. ตอบเป็นภาษาไทยเท่านั้น 2. ตอบกลับมาในรูปแบบ JSON ตามนี้เท่านั้น { "Q1" : "คำถาม", "ANS1" : "คำตอบ", "Q2" : "คำถาม", "ANS2" : "คำตอบ", "Q3" : "คำถาม" }',
    },
  ])
  result = extract_JSON(response['message']['content']) 
  result = {
    "Q1": result["Q1"],
    "ANS1": result["ANS1"],
    "Q2": result["Q2"],
    "ANS2": result["ANS2"],
    "Q3": result["Q3"]
  }
  print(result)
  end_time1 = time.time()
  print("Time: ", end_time1 - start_time1)
  
  
  print("-------------------Summary Question-------------------")
  start_time2 = time.time()
  response: ChatResponse = chat(model='scb10x/llama3.1-typhoon2-8b-instruct:latest', messages=[
    {
      'role': 'system',
      'content': f'จากข้อมูลบทสนทนาต่อไปนี้ {result} ' + 
                 'คุณเป็นผู้ช่วยที่ช่วยปรับปรุงคำถาม Q3 ให้ชัดเจนขึ้น โดยควรทำให้คำถาม Q3 ' + 
                 'รวมเนื้อหาจาก Q1 และ Q2 เข้าด้วยกันอย่างสมบูรณ์แบบ โดยไม่จำเป็นต้องอ้างอิงประวัติสนทนา ' + 
                 'ตอบกลับมาในรูปแบบ JSON ตามนี้ { "output": "" }',
    },
  ])
  
  improve_result = extract_JSON(response['message']['content']) 
  print(improve_result)
  end_time2 = time.time()
  print("Time: ", end_time2 - start_time2)
    
except Exception as e:
  print(response['message']['content'])
  print(e)
