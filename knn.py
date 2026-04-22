import random
class KNN:
    def __init__(self,k_nearest_neighbours):
        if k_nearest_neighbours%2==0:
            raise ValueError("K must be odd")
        self.k = k_nearest_neighbours
        self.data = []
        
    def train(self, data):
        self.data = data
    def test(self,data):
        self.testing = []
        for test_point in data:
            point_distances = []
            closest_points = []
            for train_point in self.data:
                dimentions = len(train_point)
                distance = 0
                for dimention in range(len(train_point)-1):
                    distance += (train_point[dimention]-test_point[dimention])**2

                point_distances.append([train_point[-1],distance])
            for i in range(self.k):
                closest_points.append(point_distances[i])
            point_distances.sort(key=lambda x: x[1])
            closest_points = point_distances[:self.k]
            class_0 = 0
            class_1 = 0
            for closest_point in closest_points:
                
                if closest_point[0] == 0:
                    class_0 += 1
                elif closest_point[0] == 1:
                    class_1 += 1                 
            if class_1 > class_0:
                self.testing.append([test_point,1])
            elif class_1 < class_0:
                self.testing.append([test_point,0])
    def accuracy(self):
        correct = 0
        total = len(self.testing)

        for result in self.testing:
            true_label = result[0][-1]   
            predicted = result[1]

            if true_label == predicted:
                correct += 1

        return correct / total if total > 0 else 0

    def precision(self):
        tp = 0
        fp = 0

        for result in self.testing:
            true_label = result[0][-1]
            predicted = result[1]

            if predicted == 1:
                if true_label == 1:
                    tp += 1
                else:
                    fp += 1

        return tp / (tp + fp) if (tp + fp) > 0 else 0

    def recall(self):
        tp = 0
        fn = 0

        for result in self.testing:
            true_label = result[0][-1]
            predicted = result[1]

            if true_label == 1:
                if predicted == 1:
                    tp += 1
                else:
                    fn += 1

        return tp / (tp + fn) if (tp + fn) > 0 else 0



training_data = []


for i in range(100):
    x = random.uniform(0, 7)
    y = random.uniform(0, 7)
    training_data.append([x, y, 0])


for i in range(100):
    x = random.uniform(3, 10)
    y = random.uniform(3, 10)
    training_data.append([x, y, 1])

test_data = []


for i in range(40):
    x = random.uniform(0, 7)
    y = random.uniform(0, 7)
    test_data.append([x, y, 0])


for i in range(40):
    x = random.uniform(3, 10)
    y = random.uniform(3, 10)
    test_data.append([x, y, 1])


model = KNN(15)
model.train(training_data)
model.test(test_data)

print("Accuracy:", model.accuracy())
print("Precision:", model.precision())
print("Recall:", model.recall())