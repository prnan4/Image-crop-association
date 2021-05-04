import json
with open('./output.json') as f1:
    output = json.load(f1)
with open('./out_res.json') as f2:
    out_res = json.load(f2)

true_pos = false_neg = false_pos = 0
for key_out in output:
    for key_out_res in out_res:
        if (key_out == key_out_res):
            list_out = output[key_out]
            list_out_res = out_res[key_out_res]
            
            if (list_out != "No crop association"):
                for i in list_out_res:
                    file_out_res = i[0]
                    flag = 0
                    for j in list_out:
                        file_out = j[0]
                        #when the crop identified in image exists in ground truth too
                        if file_out == file_out_res:
                            flag = 1
                            true_pos +=1
                     
                    #when the crop present in ground truth is not identfied in the image  
                    if (flag==0):
                        false_neg +=1
                
                #when the crop identified in image does not exist in ground truth      
                if len(list_out) > len(list_out_res):
                    false_pos += (len(list_out) - len(list_out_res))

print(true_pos, false_pos, false_neg)
precision = float(true_pos) / float(true_pos + false_pos)
recall = float(true_pos) / float(true_pos + false_neg)
print("Precision score: " + str(precision) + "\nRecall score: " + str(recall))