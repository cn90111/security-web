#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pandas as pd
import numpy as np
import math
import os
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

import json

def store(data, save_path):
    with open(save_path + '.json', 'w') as fw:
        json.dump(data,fw)
        
def load(load_path):
    with open(load_path + '.json','r') as f:
        data = json.load(f)
        return data

def show_progress(request):
    #print('show_progress------------' + str(num_progress))
    data = {
        'log':log,
        'num_progress':num_progress,
    }
    return JsonResponse(data,safe=False)


def l_diversity(request):
    
    global log
    global num_progress

    print('--------------------')
    file_name = str(request.GET.get('csv_name',None))
    inputFile = 'upload/l_Diversity/' + file_name + '/' + file_name + '.csv'
    print('--------------------')
    
    # 開啟檔案
    while(True):
        try:
            df = pd.read_csv(inputFile)
            print("開啟檔案成功")
            print('--------------------')
            print("開啟檔案 :",inputFile)
            print('--------------------')
            break
        except:
            print(inputFile,"檔案無法開啟")
            print('--------------------')
            inputFile = input("請重新輸入檔案名稱 : ")
            print('--------------------')
    
    log = "Get file success!!"
    num_progress = 20
    
    
    df
    
    attributes = list(df.columns)
    print('--------------------')
    print("all attributes :", attributes)
    print('--------------------')
    
    while(True):
        sensitiveAttribute = attributes[-1]
        #sensitiveAttribute = input("輸入Sensitive Atrribute : ")
        print('--------------------')
        if sensitiveAttribute not in list(df.columns):
            print('輸入的 Attribute 不存在，請重新輸入')
            print('--------------------')
        else:
            break
    
    log = "Get SA success!!"
    num_progress = 40
    
    
    num_data = list(df.columns[df.dtypes != object])
    
    
    
    num_data = [x for x in num_data if x not in [sensitiveAttribute]]
    
    
    num_data
    
    
    
    cate_data = list(df.columns[df.dtypes == object])
    
    
    
    cate_data = [x for x in cate_data if x not in [sensitiveAttribute]]
    
    
    
    cate_data
    
    
    
    print('--------------------')
    while(True):
        try:
            #a = input("請輸入字典檔案 :")
            a = 'upload/l_Diversity/' + file_name + '/' + file_name + '_dict'
            print('--------------------')
            dic = load(a)
            break
        except:
            print("輸入檔案錯誤! 請重新輸入")
            print('--------------------')
    
    
    # In[12]:
    log = "Get Dict File success!!"
    num_progress = 50
    
    dic
    
    cate_distance = {}
    
    for i in dic:
        each_att_distance = {}
        
        if dic[i]['type'] == 'categorical':
            
            print(i,':',dic[i]['type'],'!!!!')
            
            for j in dic[i]['structure']:
                for k in dic[i]['structure']:
                    if j == k:
                        each_att_distance[(j,k)] = 0
                    else:
                        ele = j
                        left = {ele}
                        while(dic[i]['structure'][ele]!=ele):
                            ele = dic[i]['structure'][ele]
                            left.add(ele)
                        
                        ele = k
                        right = {ele}
                        while(dic[i]['structure'][ele]!=ele):
                            ele = dic[i]['structure'][ele]
                            right.add(ele)
                            
                        jie = 1 + (len(left|right)-len(left&right))/len(left|right)
                        
                        each_att_distance[(j,k)] = math.log(jie,2)
            
            cate_distance[i] = each_att_distance
        
        else:
            print(i,':',dic[i]['type'])
                        
    
    
    cate_distance
    
    
    def find_interval(x,att):
        for i in dic[att]['interval']:
            if x >= i[0] and x <= i[1]:
                # print(i)
                return i
        print("can't find!")
    
    
    find_interval(10,'Age')
    
    
    print('--------------------')
    print('total record =',len(df))
    print('--------------------')
    
    # 輸入 K
    while(True):
        try:
            #k = int(input("輸入 k 的值 : "))
            k = int(request.GET.get('k',None))
            if(k > len(df)):
                print("k 不能比總資料數還大，請重新輸入!")
                print('--------------------')
            elif(k <= 0):
                print("k 不能為 0 或負數，請重新輸入!")
                print('--------------------')
            else:
                print('--------------------')
                print("k 合理!")
                print('--------------------')
                print("你輸入的 k =",k)
                print('--------------------')
                break
        except:
            print('--------------------')
            print("輸入格式錯誤，請重新輸入!")
            print('--------------------')
    
    log = "Get K success!!"
    num_progress = 60
    
    
    # 計算全部資料的 diversity
    diversity = {}
    for i in range(len(df)):
        diversity[df.iloc[i][sensitiveAttribute]] = 1
    total_diversity = len(diversity)
    print('--------------------')
    print('total diversity =',total_diversity)
    print('--------------------')
    print('k =',k)
    print('--------------------')
    
    # 輸入 l
    while(True):
        try:
            #l = int(input("輸入 l 的值 : "))
            l = int(request.GET.get('l',None))
            if total_diversity < l:
                print("l 不能比 total diversity 大，請重新輸入!")
                print('--------------------')
            elif l <= 0:
                print("l 不能為 0 或負數，請重新輸入!")
                print('--------------------')
            elif l > k:
                print("l 不能比 k 大，請重新輸入!")
                print('--------------------')
            else:
                print('--------------------')
                print("l 合理!")
                print('--------------------')
                print("你輸入的 l =",l)
                print('--------------------')
                break
        except:
            print('--------------------')
            print("輸入格式錯誤，請重新輸入!")
            print('--------------------')
    
    # 建立一個  tmp_df (DataFrame) 儲存
    tmp_df = pd.DataFrame(columns=list(num_data))
    
    
    tmp_df
    
    
    # 將原始資料中，資料型態為 numeric 的 Max、Min存起來
    
    # 第 0 筆存 "Max"
    # 第 1 筆存 "Min"
    
    for att in num_data:
        tmp_df.loc[0, att] = df[att].max()
        tmp_df.loc[1, att] = df[att].min()
        
    # 將"數值型資料"變成 0~1
    for i in df.index:
        for att in num_data:
            df.loc[i, att] = (df.iloc[i][att]-tmp_df.iloc[1][att])/(tmp_df.iloc[0][att]-tmp_df.iloc[1][att])
    
    
    tmp_df

    df


# 建立 Distance Matrix (numpy)
    DistanceMatrix = np.zeros((len(df),len(df)))


    DistanceMatrix


    for i in df.iterrows():
        for j in df.iterrows():
            if j[0] > i[0]:
                distance = 0
                for attribute in num_data:
                    distance = distance + ((i[1][attribute]-j[1][attribute])**2)
                for attribute in cate_data:
                    distance = distance + (cate_distance[attribute][(i[1][attribute],j[1][attribute])]**2)
                    
                distance = distance**0.5
                        
                DistanceMatrix[i[0], j[0]] = distance
                DistanceMatrix[j[0], i[0]] = distance
                
            elif i[0]==j[0]:
                distance = 0
                DistanceMatrix[i[0], j[0]] = 0
            else:
                distance = 0
                
            # print(distance)

    DistanceMatrix

    
    for att in cate_data:
        print(df[att].value_counts())
        print('------------------------')
        print(df[att].value_counts().index[0])
    
    
    # 建立中心點 center
    
    center = {}
    
    for att in num_data:
        center[att] = df[att].mean()
    for att in cate_data:
        center[att] = df[att].value_counts().index[0]

    center

# 使用 center，建立 Distance Center List (list)
    DistanceCenter = []
    for i in df.iterrows():
        distance = 0
        for att in num_data:
            distance = distance + (i[1][att]-center[att])**2
                                   
        for att in cate_data:
            distance = distance + (cate_distance[att][(i[1][att],center[att])]**2)
                                   
        distance = distance**0.5
        DistanceCenter.append(distance)
    
    DistanceCenter
    
    
    glist =[1 for i in range(len(df))]
    
    final_group = []
    upgroup_num = 1
    for x in range(len(df)):
        log = str(upgroup_num)  + "/" + str(len(df)) 
        # 檢查剩餘 ungroup 的 diversity，如果不足 l，離開此迴圈
        # 檢查剩餘 ungroup 的數量，如果不足 k，離開此迴圈
        diversity = {}
        num_ungroup = 0
        for i in range(len(df)):
            if glist[i]==1:
                num_ungroup = num_ungroup + 1
                diversity[df.iloc[i][sensitiveAttribute]] = 1
                
        current_diversity = len(diversity)
        
        if current_diversity < l or num_ungroup < k:
            break
        
        # 每次取離中心點最遠距離的點，r為此點的 index
        r = np.where(DistanceCenter==np.max(DistanceCenter))[0][0]
                                       
        # 將此點距離設為最小，以防下次又取到它
        DistanceCenter[r] = -1
        
        # 如果尚未 group
        if glist[r] == 1:
            
            # 建立一個 group
            group = []
            group.append(r)
            print('==============================')
            print('--------------------')
            print('開始第一階段(增加diversity) grouping =',group)
            print('--------------------')
            
            # 將此點設成已 group
            glist[r] = 0
            
            # 所有點與此點的距離的 list
            distance_list = list(DistanceMatrix[r])
            
            # 每次取離 r 最近距離的點，r2 為此點的 index
            r2 = np.where(distance_list==np.min(distance_list))[0][0]
            
            while distance_list[r2]!=np.inf :
                
                # 如果尚未 group
                if glist[r2] == 1:
                    
                    # 計算加入r2之前的diversity
                    diversity = {}
                    for i in group:
                        diversity[df.iloc[i][sensitiveAttribute]] = 1
                    original_diversity = len(diversity)
                        
                    # 計算加入r2之後的diversity
                    diversity[df.iloc[r2][sensitiveAttribute]] = 1
                    after_diversity = len(diversity)
                    
                    if after_diversity > original_diversity and after_diversity <= l:
                        # 加入 r2 至 group
                        group.append(r2)
                        glist[r2] = 0
                        DistanceCenter[r2] = -1
                distance_list[r2] = np.inf
                r2 = np.where(distance_list==np.min(distance_list))[0][0]
            print('完成第一階段 grouping =',group)
            print('--------------------')
            
            # extend the group
            print('開始第二階段(extend the group) grouping =',group)
            print('--------------------')
        
            for x in range(len(df)):
                d_in_list = [np.inf for i in range(len(df))]
                for i in range(len(df)):
                    in_list = []
                    
                    # 如果此點為 ungroup
                    if glist[i]==1:
                        # 計算此點至 group 所有點的距離
                        for j in group:
                            in_list.append(DistanceMatrix[i][j])
                        # 取出最小的距離作為此點的 d_in
                        d_in_list[i] = np.min(in_list)
                        
                    else:
                        # 如果此點為 group，距離設定為無限大
                        d_in_list[i] = np.inf
                            
                    # 有了目前階段所有 ungroup 點與此 group 的最小距離 (d_in_list)
                    # 取出離此 group 最接近的點 r3
                    r3 = np.where(d_in_list==np.min(d_in_list))[0][0]
                
                    while d_in_list[r3]!=np.inf:
                    
                        # 檢查是否能加入
                    
                        # 計算此點r3至其他ungroup點的最小距離
                        out_list = [np.inf]
                        for i in range(len(df)):
                            if glist[i] == 1 and i!=r3:
                                out_list.append(DistanceMatrix[r3][i])
                        d_out = np.min(out_list)
                    
                        if d_out == np.inf:
                            # 剩下此點
                            break
                    
                        # 計算加入r3之前的diversity
                        diversity = {}
                        for i in group:
                            diversity[df.iloc[i][sensitiveAttribute]] = 1
                        original_diversity = len(diversity)
                    
                        # 計算加入r3之後的diversity
                        diversity[df.iloc[r3][sensitiveAttribute]] = 1
                        after_diversity = len(diversity)
                
                        if after_diversity>=original_diversity and d_out > d_in_list[r3]:
                            # 加入此點 r3
                            group.append(r3)
                            glist[r3] = 0
                            d_in_list[r3] = np.inf
                        else:
                            # 不能加入此點 r3
                            d_in_list[r3] = np.inf
                            r3 = np.where(d_in_list==np.min(d_in_list))[0][0]
            print('完成第二階段 grouping =',group)
            print('--------------------')
            
            print('開始第三階段(extend the size to k) grouping =',group)
            print('--------------------')
        
            if len(group) < k:
                
                # 取得所有點至此 group 的最小距離的 list
                min_distance_list = []
                
                for i in range(len(df)):
                    
                    # 如果此點已 group
                    if glist[i] == 0:
                        min_distance_list.append(np.inf)
                    else:
                        tmp_list = []
                        
                        # 將點 i 與 group 中所有點的距離蒐集起來
                        for j in group:
                            tmp_list.append(DistanceMatrix[i][j])
                        
                        # 取最小距離
                        min_distance_list.append(min(tmp_list))
                
                # 再加入 k-len(group) 個點即可
                for i in range(k-len(group)):
                    
                    # 取得與此 group 距離最近的點
                    r5 = np.where(min_distance_list==np.min(min_distance_list))[0][0]
                    
                    # 如果此點已經被 group，代表全部都為 np.inf ，代表無法再找
                    while glist[r5]==0:
                        print("有問題喔!!!XDD!!!!")
                        min_distance_list[r5] = np.inf
                        r5 = np.where(min_distance_list==np.min(min_distance_list))[0][0] 
                    
                    # r5 為距離此 group 最近的未 group 的點，將 r5 加入此 group
                    group.append(r5)
                    min_distance_list[r5] = np.inf
                    glist[r5] = 0
                    
            print('完成第三階段 grouping =',group)
            print('--------------------')            
        
            # 將 group 放入 final_group清單中
            final_group.append(group)
            print('放入final group中')
            print('--------------------')
            upgroup_num = upgroup_num + 1

        
    # 將剩下 ungroup 的點加入鄰近的 group
    print('==============================')
    print('--------------------')
    print('最後階段，將剩下 ungroup 的資料加入鄰近的 grouping')
    print('--------------------')
    for i in range(len(df)):
        
        # 如果此點為 ungroup
        if glist[i] == 1:
            
            # 取得此點與所有點的距離
            distance_list = list(DistanceMatrix[i])
            
            # 取得與此點距離最近的點
            r4 = np.where(distance_list==np.min(distance_list))[0][0]
            
            # 如果此點尚未被 group，找下一個
            while glist[r4]==1 and distance_list[r4]!=np.inf:
                distance_list[r4] = np.inf
                r4 = np.where(distance_list==np.min(distance_list))[0][0]
            
            # r4 為距離 i 最近的已 group 的點，將 i 加入 r4 的 group
            for group in final_group:
                if r4 in group:
                    group.append(i)
                    glist[i] = 0
    print('結束最後階段')
    print('--------------------')
    print('所有的 group :')
    for g in final_group:
        print(g)
    print('--------------------')
    
    a = 0
    for g in final_group:
        a = a + len(g)
        
    print('total record after grouping =',a)
    print('--------------------')

    final_group

    output_df_with_dic = pd.DataFrame(columns=list(df.columns))

    output_df_with_dic

# 重新開啟檔案 (因為標準化時有更動到原始資訊)
    df = pd.read_csv(inputFile)


# 檢查每個 group 是否符合 k l
    print('檢查每個 group 是否符合 K & L')
    print('--------------------')
    
    for g in final_group:
        print('group =',g,':')
        if len(g) >= k:
            print('   符合 K !')
        else:
            print('   不符合 K !')
        
        diversity = {}
        for i in g:
            diversity[df.iloc[i][sensitiveAttribute]] = 1
        if len(diversity) >= l:
            print('   符合 L !')
        else:
            print('   不符合 L !')
        print('--------------------')


    def process_df(df):
        
        
        tmp_df = df.copy()
        
        for c in num_data+cate_data:
            if dic[c]['type']=='categorical':
                check = tmp_df.at[tmp_df.index[0], c]
                a=sum(tmp_df[c] == check)
                while(a!= len(tmp_df)):
                    tmp_df[c] = tmp_df[c].map(lambda x: dic[c]['structure'][str(x)])
                
                    check = tmp_df.at[tmp_df.index[0], c]
                    a=sum(tmp_df[c] == check)
            else:
                min_value = find_interval(tmp_df[c].min(),c)[0]
                max_value = find_interval(tmp_df[c].max(),c)[1]
                
                tmp_df[c] = tmp_df[c].map(lambda x: str(min_value)+'-'+str(max_value))
                
        return tmp_df
        

# 印出結果
    for group in final_group:
        
        tmp_df = pd.DataFrame(columns=list(df.columns))
        
        for i in group:
            tmp_df = tmp_df.append(df.iloc[i], ignore_index=True)
        
        tmp_df = process_df(tmp_df)
        
        for i in range(len(tmp_df)):
            output_df_with_dic = output_df_with_dic.append(tmp_df.iloc[i], ignore_index=True)
        print('---------------------------------------')
        print(tmp_df)
    print('---------------------------------------')
# In[42]:


# 設定顯示全部資料
    pd.set_option('display.max_rows',None)
    if not os.path.isdir('output/l_Diversity/' + file_name + '/'):
        os.makedirs('output/l_Diversity/' + file_name + '/')
    output_df_with_dic.to_csv('output/l_Diversity/' + file_name + '/' +  file_name + '_output.csv', encoding='cp950', index=False, columns=list(df.columns))
    
    log = "All Success!!"
    num_progress = 100
    
    
    dic['Age']['interval']

    return JsonResponse(num_progress, safe=False)



