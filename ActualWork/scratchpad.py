'''
x=2
if not x==2 and x==3:
    print("this works as expected")
'''

x = 12
if not x:
    print("HI")

list = []
for element in list:
    print("Don't break!")

'''
for triangle in tripy.earclip(pointlist(linecoordsx,linecoordsy)):
        for i in range(-1,2):
            shapes.Line(triangle[i][0],triangle[i][1],triangle[i+1][0],triangle[i+1][1],color=(100,100,100),width=1).draw()
'''

# for point in vertices:
#             vert = dict[point]
#             if vert.edgeList != [] and vert!= path_tree.root:
#                 print("hello! I am", vert,"with",vert.edgeList)
        

# for v in polygon:
#         v_a = cch.dict_a[v]
#         cch.addCoarse(v_a,a,final_cover)
#         v_b = cch.dict_b[v]
#         cch.addCoarse(v_b,b,final_cover)
#         u_a = v_a.parent
#         u_b = v_b.parent
#         # if cch.isVisible(v) and u_a.cds()!=a:
#         #     Ia = (cch.X_a(u_a.cds(),a),cch.X_a(v))
#         #     fa = CoarseFunct(1,u_a.cds(),dist(u_a.cds(),v_a.cds()+v_a.far_length))
#         #     Ha = v_a.far_edge
#         #     final_cover.append(Triple(Ia,fa,Ha))
#         # if cch.isVisible(v) and u_b.cds()!=b:
#         #     Ib = (cch.X_a(u_b.cds()),cch.X_a(v))
#         #     fb = CoarseFunct(1,u_b.cds(),dist(u_b.cds(),v_b.cds()+v_b.far_length))
#         #     Hb = v_b.far_edge
#         #     final_cover.append(Triple(Ia,fa,Ha))