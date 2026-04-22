import math
lr=0.0001 # Learning rate
error_margin = 0.01 # Accuracy
guess_buy_m1, guess_buy_m2, guess_buy_m3, guess_buy_m4, guess_buy_c, guess_not_buy_m1, guess_not_buy_m2, guess_not_buy_m3, guess_not_buy_m4, guess_not_buy_c = (1,)*10 # Initial assumptions
data = [ # Data provided
    [23, 180, 3, 85, 1],
    [28, 160, 3, 75, 1],
    [35, 150, 4, 90, 1],
    [32, 140, 3, 80, 1],
    [38, 155, 4, 95, 1],
    [26, 170, 3, 88, 1],

    [45, 95,  2, 55, 0],
    [50, 80,  2, 50, 0],
    [42, 90,  2, 60, 0],
    [48, 85,  2, 52, 0],
    [40, 100, 3, 65, 0],
    [46, 88,  2, 58, 0],
]


data_to_be_predicted= [34, 150, 3, 85] # Data for the value to be found

def func_buy(x,y,z,a): # Function for score to buy
    return guess_buy_m1 * x + guess_buy_m2 * y + guess_buy_m3 * z + guess_buy_m4 * a + guess_buy_c
def func_not_buy(x,y,z,a): # Function for score not to buy
    return guess_not_buy_m1 * x + guess_not_buy_m2 * y + guess_not_buy_m3 * z + guess_not_buy_m4 * a + guess_not_buy_c

def loss(p,y): # Loss function
    eps = 1e-15  # tiny value
    p = max(min(p, 1 - eps), eps)
    return -(y*math.log(p)+(1-y)*math.log(1-p)) # Loss formula
def softmax(scores):
    max_score = max(scores)
    exp_scores = [math.exp(s - max_score) for s in scores]
    total = sum(exp_scores)
    return [s / total for s in exp_scores]


def error(): # Function to detect errors
    # Error lists
    errors_buy, errors_not_buy = [], []
    dm1_buy_contributions, dm2_buy_contributions, dm3_buy_contributions, dm4_buy_contributions, dc_buy_contributions = [], [], [], [], []
    dm1_not_buy_contributions, dm2_not_buy_contributions, dm3_not_buy_contributions,            dm4_not_buy_contributions, dc_not_buy_contributions = [], [], [], [], []
    
    

    for list in data:
        a,b,c,d,y = list  # Value per Point per data
        global scores 
        scores = [func_buy(a,b,c,d),func_not_buy(a,b,c,d)]
        if y == 1:
            p_buy = (guess_buy_m1*a+guess_buy_m2*b+guess_buy_m3*c+guess_buy_m4*d+guess_buy_c)
            error_buy = p_buy - y
            errors_buy.append(error_buy)
            dm1_buy_contributions.append(error_buy * a)
            dm2_buy_contributions.append(error_buy * b)
            dm3_buy_contributions.append(error_buy * c)
            dm4_buy_contributions.append(error_buy * d)
            dc_buy_contributions.append(error_buy)
        else:
            p_not_buy = (guess_not_buy_m1*a+guess_not_buy_m2*b+guess_not_buy_m3*c+guess_not_buy_m4*d+guess_not_buy_c)
            error_not_buy = (p_not_buy-(1-y))
            errors_not_buy.append(error_not_buy)
            dm1_not_buy_contributions.append(error_not_buy * a)
            dm2_not_buy_contributions.append(error_not_buy * b)
            dm3_not_buy_contributions.append(error_not_buy * c)
            dm4_not_buy_contributions.append(error_not_buy * d)
            dc_not_buy_contributions.append(error_not_buy)
    # Returns list of average error per type
    return [sum(errors_buy)/len(errors_buy),sum(errors_not_buy)/len(errors_not_buy), sum(dm1_buy_contributions)/len(dm1_buy_contributions), sum(dm2_buy_contributions)/len(dm2_buy_contributions), sum(dm3_buy_contributions)/len(dm3_buy_contributions), sum(dm4_buy_contributions)/len(dm4_buy_contributions), sum(dc_buy_contributions)/len(dc_buy_contributions),sum(dm1_not_buy_contributions)/len(dm1_not_buy_contributions), sum(dm2_not_buy_contributions)/len(dm2_not_buy_contributions), sum(dm3_not_buy_contributions)/len(dm3_not_buy_contributions), sum(dm4_not_buy_contributions)/len(dm4_not_buy_contributions), sum(dc_not_buy_contributions)/len(dc_not_buy_contributions)]

 
for i in range(10000000): # 10,000,000 iterations of attempting
    # Gradient descent logic
    current_buy_error,current_not_buy_error, dm1_buy, dm2_buy, dm3_buy, dm4_buy, dc_buy, dm1_not_buy, dm2_not_buy, dm3_not_buy,dm4_not_buy, dc_not_buy = error()

        
    probs = softmax(scores)
    # Gradient for each class = predicted - true
    grad_buy     = probs[0] - 1
    grad_not_buy = probs[1]

    guess_buy_m1-= lr * grad_buy * dm1_buy
    guess_buy_m2-= lr * grad_buy * dm2_buy
    guess_buy_m3-= lr * grad_buy * dm3_buy
    guess_buy_m4-= lr * grad_buy * dm4_buy
    guess_buy_c-= lr * grad_buy * dc_buy

    guess_not_buy_m1-= lr * grad_not_buy * dm1_not_buy
    guess_not_buy_m2-= lr * grad_not_buy * dm2_not_buy
    guess_not_buy_m3-= lr * grad_not_buy * dm3_not_buy
    guess_not_buy_m4-= lr * grad_not_buy * dm4_not_buy
    guess_not_buy_c-= lr * grad_not_buy * dc_not_buy


    # Announcment per 20,000 iterations of attempts to inspect value 
    if i % 20000 == 0:
        print(f"Current guesses: predicted score = {softmax(scores)}, i = {i}, error_buy = {error()[0]}, error_not_buy = {error()[1]}")
    # Stops for loop if error margin is too tiny
    if error()[0]< error_margin and error()[1]< error_margin:   
        break

# Final prediction
print(softmax(scores))        
                