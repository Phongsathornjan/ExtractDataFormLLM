# -*- coding: utf-8 -*-
import time
import pandas as pd
from ollama import chat
from ollama import ChatResponse

from extract_JSON import extract_JSON

try:
  
  final_result = []
  
  file_path = 'Q_Dataset.xlsx'
  df = pd.read_excel(file_path, usecols='A')
  test = 0
  for index, value in df.iterrows():
    if index < 202:
      continue
    start_time1 = time.time()
    # print("-------------------Generate Question-------------------")
    response: ChatResponse = chat(model='scb10x/llama3.1-typhoon2-8b-instruct:latest', messages=[
      {
        'role': 'system',
        'content': f'คุณเป็นผู้ใช้งานทั่วไปที่กำลังสนทนากับ chatbot เพื่อถามคำถามเกี่ยวกับ {value.iloc[0]} 3 คำถามสั้นๆ '+'โดยคำถามถัดจากคำถามแรก เป็นการถามต่อเพื่อขยายความจากคำถามก่อนหน้าสั้นๆ กระชับ และเป็นธรรมชาติ **กฏ** 1. ตอบเป็นภาษาไทยเท่านั้น 2. ตอบกลับมาในรูปแบบ JSON ตามนี้เท่านั้น { "Q1" : "คำถาม", "ANS1" : "คำตอบ", "Q2" : "คำถาม", "ANS2" : "คำตอบ", "Q3" : "คำถาม" }',
      },
    ])
    
    result = extract_JSON(response['message']['content'])
    if(result == None):
      continue
      
    result = {
      "Q1": result["Q1"],
      "ANS1": result["ANS1"],
      "Q2": result["Q2"],
      "ANS2": result["ANS2"],
      "Q3": result["Q3"]
    }
    # print(result)
    end_time1 = time.time()
    time1 = end_time1 - start_time1
    # print("Time: ", time1)
    
    
    # print("-------------------Summary Question-------------------")
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
    if(improve_result == None):
      continue 
    
    # print(improve_result)
    end_time2 = time.time()
    time2 = end_time2 - start_time2
    # print("Time: ", time2)

    final_result.append({
      "Q1": result["Q1"],
      "ANS1": result["ANS1"],
      "Q2": result["Q2"],
      "ANS2": result["ANS2"],
      "Q3": result["Q3"],
      "output" : improve_result["output"],
      "Time_Process1" : time1,
      "Time_Process2" : time2,
      "Total Time" : time1 + time2
    })
  
    print(f"----------------QA{index}----------------")
    print(final_result[index])

    test+= 1
    if(test == 500):
      break
    
  print("-------------------SUCCESS-------------------")
  
  # สร้าง DataFrame จากข้อมูล
  df = pd.DataFrame(final_result)

  # บันทึก DataFrame ลงใน Excel
  df.to_excel("QA_Dataset.xlsx", index=False)
  
except Exception as e:
  print(response['message']['content'])
  print(e)
  
    # สร้าง DataFrame จากข้อมูล
  df = pd.DataFrame(final_result)

  # บันทึก DataFrame ลงใน Excel
  df.to_excel("QA_Dataset.xlsx", index=False)
