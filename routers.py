
import random
from MinimumSpanningTree import *



def find_distance(source,points):
    dns = {}
    print(points)
    for point in points:
        dns[point] = max(abs(source[0]-point[0]),abs(source[1] - point[1]))
    return dns

def find_distance2(source,point):
    return max(abs(source[0]-point[0]),abs(source[1] - point[1]))


def find_backbone_path(genetic_list):
    global init
    all_dns = {}
    bgn =[]
    bgn.append(init)
    bgn.extend(genetic_list)
    cpg = list(bgn[:])
    for point in bgn:
        print(point)
        print(cpg)
        cpg.remove(point)
        print(cpg)
        all_dns[point] = find_distance(point,cpg)
        cpg.append(point)
    return MinimumSpanningTree(all_dns)

def valuation(genetic_list):
    cost = 0
    bpath = find_backbone_path(genetic_list)
    for subpath in bpath:
        cost += find_distance2(subpath[0],subpath[1])*Pb
    return cost


def target_id_covered(pos,routers):
    for rpos in routers:
        if abs(pos[0] - rpos[0]) <= R and abs(pos[1] - rpos[1]) <= R:
            return True;


def print_coverage(routers):
    global grid
    num = 0
    for pos in valid_coordinates:
            if target_id_covered(pos,routers):
                num+=1
                grid[pos[0]][pos[1]] = 'x'
    for router in routers:
        grid[router[0]][router[1]] = "r"
    return num

def coverage(routers):
    num = 0
    for pos in valid_coordinates:
        if target_id_covered(pos,routers):
            num += 1
    return float(num)/len(valid_coordinates)


def reput(genetic_list):
    for i in range(len(genetic_list)):
        vcoor.append(genetic_list[i])
        rc = random.choice(vcoor)
        genetic_list[i] = rc
        vcoor.remove(rc)

def free(genetic_list):
    global cur_budget
    for i in range(len(genetic_list)):
        if( random.choice([0,1]) == 1):
            key = random.choice(range(len(genetic_list)))
            vcoor.append(genetic_list[key])
            del genetic_list[key]
            cur_budget += Pr

def add(genetic_list):
    global cur_budget
    if( random.choice([0,1]) == 1):
        rc = random.choice(vcoor)
        genetic_list.append((rc)) # (position)
        vcoor.remove(rc)
        cur_budget -= Pr

def renew(genetic_list):
    while (cur_budget < 0):
        free(genetic_list)
    add(genetic_list)
    reput(genetic_list)




def init_list_sol():
    global cur_budget
    genetic_list = []
    #x = [1]
    probs = [1,0,0,0,0]#x.extend([ 0 for i in range(R*R)])
    print("Starting...")
    for i in range(max_routers):
        if random.choice(probs) == 1:
            print("Inital random choice...")
            rc = random.choice(vcoor)
            print("I choosed the: " + str(rc))
            genetic_list.append((rc)) # (position)
            print("Genetic List: " + str(genetic_list))
            vcoor.remove(rc)
            cur_budget -= Pr
            print("cur budget: " + str(cur_budget))
    return genetic_list


def genetic_alg(genetic_list):
    global cur_budget
    print("Genetic algorithm starts...")
    while True:
        for i in range(10):
            print("Calculating valuation...")
            val = valuation(genetic_list)
            cur_budget -= val
            print("cur_budget: " + str(cur_budget))
            cv = coverage(genetic_list)
            print("Coverage: " + str(cv))
            if(cv >= 0.85 and cur_budget >=0):
                print("TERMINATE!")
                return genetic_list,cv
            print("Reputing...")
            cur_budget += val
            reput(genetic_list)
        else:
            print("Renewing...")
            renew(genetic_list)




input_file = open("input.in")
content = input_file.read().splitlines()
rows,cols,R = [int(x) for x in content[0].split()]
Pb,Pr,B= [int(x) for x in content[1].split()]
init = tuple( [ int(x) for x in content[2].split()])
grid = [ list(z) for z in content[3:]]

valid_coordinates =[]
for i in range(rows):
    for j in range(cols):
        if(grid[i][j] == "."):
            valid_coordinates.append((i,j))
vcoor = valid_coordinates[:]
#print(valid_coordinates)

max_routers = int(B/Pr)
cur_budget = B
genetic_list = init_list_sol()
print(genetic_list)
print("Result:")

final_routers, cov = genetic_alg(genetic_list)

xz = print_coverage(final_routers)

for line in grid:
    print(line)
print("Coverage: " + str(cov))
print("Number of covered points: " + str(xz))
