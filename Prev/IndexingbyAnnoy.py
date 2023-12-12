from annoy import AnnoyIndex

f = 1536

t = AnnoyIndex(f, 'angular')
for i in range(len(embedding_dic)):
  value = embedding_dic[i]
  t.add_item(i, value)

t.get_item_vector(52)
t.build(10) # 10 trees
t.save('test.ann')

u = AnnoyIndex(f, 'angular')
u_loader = u.load('test.ann')