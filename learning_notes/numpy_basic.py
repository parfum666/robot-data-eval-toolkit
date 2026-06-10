import numpy as np

rewards = np.array([[20,30,40],
                   [40,40,50],
                   [10,20,30],
 ]                  )
print(rewards)

print (type(rewards))

print("mean:",rewards.mean())
print("max:",rewards.max())
print("min:",rewards.min())
print("shape:",rewards.shape)
print("sun:",rewards.sum())

print(rewards[:,1])
print(rewards[1,:])
print(rewards[0:2,0:2])
