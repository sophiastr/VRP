from Model import *
import math
import copy
import random

class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = None
        self.profit = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9
        self.profit = - 10 ** 9
class SwapMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None
        self.profit = None
    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9
        self.profit = -10 ** 9
class TwoOptMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = None
        self.profit = None
    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9
        self.profit = -10 ** 9
class ExchangeMove(object):
    def __init__(self):
        self.positionOfRoute = None
        self.positionOfNode = None
        self.moveCost = None
        self.node = None
        self.profit = None
    def Initialize(self):
        self.positionOfRoute = None
        self.Node = None
        self.positionOfNode = None
        self.moveCost = 10 ** 9
        self.profit = -10 ** 9
class Solution:
    def __init__(self):
        self.profit = 0
        self.routes = []
        for i in range(6):
            self.routes.append(Route((23.142, 11.736)))
        self.visited = set()
        self.visited.add((23.142, 11.736))
        self.tabu = {}
class CustomerInsertionAllPositions():
    def __init__(self):
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.dz = 10 ** 9
        self.min = 10 ** 9
        self.profit = - 10 ** 9
class Solver:
    def __init__(self, m):
        self.allNodes = {}
        self.allNodes = m.allNodes
        self.depot = (23.142, 11.736)
        self.number_of_routes = m.number_of_routes
        self.sol = None
        self.bestSolution = None
        self.overallBestSol = None
        self.rcl_size = 2
        self.rcl_size2 = 2
    def solve(self):
        random.seed(30)
        final = []
        profit = 0
        thesi = -1
        for i in range(28):
            self.sol = Solution()
            for k, y in self.allNodes.items():
                self.sol.tabu[k] = 0
            flag = True
            while flag:
                flag = self.ApplyNearestNeighborMethod()
            for t in range(6):
                self.sol.routes[t].time = self.sol.routes[t].time + math.dist(
                    (self.sol.routes[t].sequenceOfNodes[-1]), (23.142, 11.736))
                self.sol.routes[t].sequenceOfNodes.append((23.142, 11.736))
            flag = True
            while flag:
                flag = self.MinimumInsertions(self.sol)
            #self.LocalSearch(1)

            #self.VND()
            self.TabuSearch()
            self.Exchange()
            if profit == 0 or profit < self.sol.profit and self.CalculateTotalCostAndCapacity():
                thesi = i
                final = []
                profit = self.sol.profit
                for t in range(6):
                    view = []
                    for node in self.sol.routes[t].sequenceOfNodes:
                        for key, values in self.allNodes.items():
                            if node == key:
                                view.append(values[0])
                    final.append(view)
        self.reportfinalsoloution(profit, final, thesi)
        return self.sol
    def reportfinalsoloution(self, profit, final, thesi):
        count = 1
        f= open("solution.txt","w+")
        print("Total Profit")
        f.write("Total Profit\n")
        print(profit)
        f.write("%d\r" % (profit))
        count = 1
        for i in final:
            count2 = 0
            f.write("Route %d\r" % (count))
            print("Route ", count)
            print(*i)
            for k in i:
                if count2 == (len(i)-1):
                    f.write("%d\r" %(k))
                else:
                    f.write("%d " % (k))
                count2 += 1
            count += 1
        f.close()
    def reportSolution(self, solution):
        print("Total Profit")
        print(solution.profit)
        for t in range(6):
            view = []
            print("Route", t + 1)
            for node in solution.routes[t].sequenceOfNodes:
                for key, values in self.allNodes.items():
                    if node == key:
                        view.append(values[0])
            print(*view)
    def ApplyNearestNeighborMethod(self):
        flag = False
        rcl = []
        # για κάθε ανοικτή/δυνατή διαδρομή(έξι):
        for i in range(self.number_of_routes):
            last = self.sol.routes[i].sequenceOfNodes[-1]
            # για κάθε κόμβο
            for key, values in self.allNodes.items():
                distance = math.dist((last), (key[0], key[1]))
                distance_return = math.dist((key[0], key[1]), (self.depot))
                if (key[0], key[1]) not in self.sol.visited and distance + distance_return + values[2] + \
                        self.sol.routes[i].time <= 130 and values[1] + self.sol.routes[
                    i].capacity <= 90 and values[2] / values[1] < 1.2 and values[1] / values[3] < 1.1:
                    flag = True
                    deiktis = (values[3]) / (distance + values[2])
                    route = i
                    dist = distance
                    node = (key[0], key[1])
                    if len(rcl) < self.rcl_size:
                        new_tup = (deiktis, node, route, dist)
                        rcl.append(new_tup)
                        rcl.sort(key=lambda x: x[0], reverse=True)
                    elif deiktis > rcl[-1][0]:
                        rcl.pop(len(rcl) - 1)
                        new_tup = (deiktis, node, route, dist)
                        rcl.append(new_tup)
                        rcl.sort(key=lambda x: x[0], reverse=True)
        if flag:
            tup_index = random.randint(0, len(rcl) - 1)
            tpl = rcl[tup_index]
            route = tpl[2]
            node = tpl[1]
            dist = tpl[3]
            self.sol.routes[route].sequenceOfNodes.append(node)
            self.sol.routes[route].time = self.sol.routes[route].time + dist + self.allNodes[node][2]
            self.sol.routes[route].capacity = self.sol.routes[route].capacity + self.allNodes[node][1]
            self.sol.profit = self.sol.profit + self.allNodes[node][3]
            self.sol.visited.add(node)
        return flag
    def ApplyCustomerInsertionAllPositions(self, insertion, solution):
        node = insertion.customer
        rt = insertion.route
        # before the second depot occurrence
        insIndex = insertion.insertionPosition
        rt.sequenceOfNodes.insert(insIndex + 1, node)
        rt.time = rt.time + self.allNodes[node][2] + insertion.dz
        rt.capacity = rt.capacity + self.allNodes[node][1]
        solution.profit += self.allNodes[node][3]
        self.sol.visited.add(node)
    def MinimumInsertions(self, solution):
        bestInsertion = CustomerInsertionAllPositions()
        flag = False
        count = 0
        for key, values in self.allNodes.items():
            if (key[0], key[1]) not in self.sol.visited and values[2] / values[1] < 1.2 and values[1] / values[3] < 1.1:
                for route in solution.routes:
                    flag = self.IdentifyBestInsertionAllPositions(bestInsertion, route, (key[0], key[1]))
                    if flag == True:
                        count = count + 1
        if count > 0:
            flag = True
            self.ApplyCustomerInsertionAllPositions(bestInsertion, solution)
        return flag
    def IdentifyBestInsertionAllPositions(self, bestInsertion, rt, node):
        flag = False
        if rt.capacity + self.allNodes[(node)][1] <= 150:
            for j in range(0, len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[j]
                B = rt.sequenceOfNodes[j + 1]
                costAdded = math.dist(A, node) + math.dist(B, node)
                costRemoved = math.dist(A, B)
                trialCost = costAdded - costRemoved

                if rt.time + self.allNodes[node][2] + trialCost <= 200:
                    flag = True
                    deiktis = (trialCost + self.allNodes[node][1] + self.allNodes[node][2])/self.allNodes[node][3]
                    if deiktis < bestInsertion.min:
                        bestInsertion.min = (trialCost + self.allNodes[node][1] + self.allNodes[node][2])/self.allNodes[node][3]
                        bestInsertion.dz = trialCost
                        bestInsertion.route = rt
                        bestInsertion.customer = node
                        bestInsertion.insertionPosition = j

        return flag
    def TabuSearch(self):
        self.bestSolution = self.cloneSolution(self.sol)
        for i in range(len(self.sol.routes)):
            self.bestSolution.routes[i] = copy.copy(self.sol.routes[i])
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()
        sm = SwapMove()
        top: TwoOptMove = TwoOptMove()

        while terminationCondition is False:
            operator = random.randint(0, 3)

            rm.Initialize()
            sm.Initialize()
            top.Initialize()

            # Relocations
            if operator == 0:
                self.FindBestRelocationMove2(rm, localSearchIterator)
                if rm.originRoutePosition is not None:
                    self.ApplyRelocationMove2(rm, localSearchIterator)
                    flag = True
                    while flag:
                        flag = self.MinimumInsertions2(self.sol)

            # Swaps
            elif operator == 1:
                self.FindBestSwapMove2(sm, localSearchIterator)
                if sm.positionOfFirstRoute is not None:
                    self.ApplySwapMove2(sm, localSearchIterator)
                    flag = True
                    while flag:
                        flag = self.MinimumInsertions2(self.sol)
            elif operator == 2:
                self.FindBestTwoOptMove2(top, localSearchIterator)
                if top.positionOfFirstRoute is not None:
                    self.ApplyTwoOptMove2(top, localSearchIterator)
                    flag = True
                    while flag:
                        flag = self.MinimumInsertions2(self.sol)

            # self.ReportSolution(self.sol)
            #self.TestSolution()
            #solution_cost_trajectory.append(self.sol.cost)

            #print(localSearchIterator, self.sol.profit, self.bestSolution.profit)
            if (self.sol.profit < self.bestSolution.profit):
                self.sol = self.cloneSolution(self.bestSolution)


            localSearchIterator = localSearchIterator + 1

            if localSearchIterator > 8:
                terminationCondition = True
    def VND(self):
        self.bestSolution = self.cloneSolution(self.sol)
        VNDIterator = 0
        kmax = 2
        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        ex = ExchangeMove()
        k = 0

        while k <= kmax:
            self.InitializeOperators(rm, sm, top, ex)
            if k == 1:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None and rm.profit > 0:
                    self.ApplyRelocationMove(rm)
                    flag = True
                    while flag:
                        flag = self.MinimumInsertions2(self.sol)
                    VNDIterator = VNDIterator + 1
                    k = 0
                else:
                    k += 1

            elif k == 0:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None and sm.profit > 0:
                    self.ApplySwapMove(sm)
                    flag = True
                    while flag:
                        flag = self.MinimumInsertions2(self.sol)
                    VNDIterator = VNDIterator + 1
                    k = 0
                else:
                    k += 1
            elif k == 2:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None and top.profit > 0:
                    self.ApplyTwoOptMove(top)
                    flag = True
                    while flag:
                        flag = self.MinimumInsertions2(self.sol)
                    VNDIterator = VNDIterator + 1
                    k = 0
                else:
                    k += 1
            if (self.sol.profit > self.bestSolution.profit):
                self.bestSolution = self.cloneSolution(self.sol)
    def LocalSearch(self, operator):
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        ex = ExchangeMove()
        while terminationCondition is False:

            self.InitializeOperators(rm, sm, top, ex)
            # Relocations
            if operator == 1:
                self.FindeBestExchangeMove(ex)
                if ex.positionOfRoute is not None:
                    if ex.profit > 0:
                        self.ApplyBestExchangeMove(ex)
                        flag = True
                        while flag:
                            flag = self.MinimumInsertions2(self.sol)
                    else:
                        terminationCondition = True
            elif operator == 2:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.profit > 0:
                        self.ApplySwapMove(sm)
                        flag = True
                        while flag:
                            flag = self.MinimumInsertions2(self.sol)
                    else:
                        terminationCondition = True
            elif operator == 0:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None:
                    if top.profit > 0:
                        self.ApplyTwoOptMove(top)
                        flag = True
                        while flag:
                            flag = self.MinimumInsertions2(self.sol)
                    else:
                        terminationCondition = True

            if (self.sol.profit > self.bestSolution.profit):
                self.bestSolution = self.cloneSolution(self.sol)
    def cloneRoute(self, rt: Route):
        cloned = Route(self.depot)
        cloned.time = rt.time
        cloned.capacity = rt.capacity
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned
    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            clonedRoute = self.cloneRoute(rt)
            cloned.routes.append(clonedRoute)
        cloned.profit = self.sol.profit
        return cloned
    def InitializeOperators(self, rm, sm, top, ex):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()
        ex.Initialize()
    def FindBestRelocationMove2(self, rm, iterator):
        profit = 0
        for originRouteIndex in range(0, len(self.sol.routes)):
            rt1:Route = self.sol.routes[originRouteIndex]
            for targetRouteIndex in range(0, len(self.sol.routes)):
                rt2:Route = self.sol.routes[targetRouteIndex]
                for originNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    for targetNodeIndex in range(0, len(rt2.sequenceOfNodes) - 1):

                        if originRouteIndex == targetRouteIndex and (targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        if rt1 != rt2:
                            if rt2.capacity + self.allNodes[B][1] > 150:
                                continue
                        costAdded = math.dist(A,C) + math.dist(F, B) + math.dist(B, G)
                        costRemoved = math.dist(A, B) + math.dist(B, C) + math.dist(F, G)
                        originRtCostChange = math.dist(A, C) - math.dist(A, B) - math.dist(B, C) - self.allNodes[B][2]
                        targetRtCostChange = math.dist(F, B) + math.dist(B, G) - math.dist(F, G) + self.allNodes[B][2]
                        moveCost = costAdded - costRemoved
                        #ΣΤΟ ΜΟΥΒ ΚΟΣΤ ΥΠΟΛΟΓΙΣΕ ΚΑΙ ΤΟΥΣ ΧΡΟΝΟΥΣ ΕΞΥΠΗΡΕΤΗΣΕΙΣ ΩΣΤΕ ΝΑ ΕΙΝΑΙ ΑΡΝΗΤΙΚΟΙ
                        if rt1 != rt2:
                            if rt2.time + targetRtCostChange > 200:
                                continue
                        if rt1 == rt2:
                            if moveCost < 0:
                                new_route1 = []
                                for nodes in self.sol.routes[originRouteIndex].sequenceOfNodes:
                                    new_route1.append(nodes)
                                del new_route1[originNodeIndex]
                                if (originNodeIndex < targetNodeIndex):
                                    new_route1.insert(targetNodeIndex, B)
                                else:
                                    new_route1.insert(targetNodeIndex + 1, B)
                                profit = self.CheckMaxProfit(new_route1, rt1.time + moveCost, self.sol.routes[originRouteIndex].capacity)

                        else:
                            if moveCost < 0:
                                new_route1 = []
                                new_route1= rt1.sequenceOfNodes.copy()
                                del new_route1[originNodeIndex]
                                profit = self.CheckMaxProfit(new_route1, rt1.time + originRtCostChange, rt1.capacity - self.allNodes[B][1])
                                new_route2 = []
                                new_route2 = rt2.sequenceOfNodes.copy()
                                new_route2.insert(targetNodeIndex + 1, B)
                                profit2 = self.CheckMaxProfit(new_route2, rt2.time + targetRtCostChange, rt2.capacity + self.allNodes[B][1])
                                if profit2 > profit:
                                    profit = profit2
                        if (self.MoveIsTabu(B, iterator, profit)):
                            continue
                        if (profit  + ((-1) * moveCost/4)> rm.profit):
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm, profit + ((-1) * moveCost/4))
    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm:RelocationMove, profit):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost
        rm.profit = profit
    def ApplyRelocationMove2(self, rm: RelocationMove,iterator):
        originRt = self.sol.routes[rm.originRoutePosition]
        targetRt = self.sol.routes[rm.targetRoutePosition]

        B = originRt.sequenceOfNodes[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)

            originRt.time += rm.moveCost
        else:
            #(18.553, 6.847)
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.time += rm.costChangeOriginRt
            targetRt.time += rm.costChangeTargetRt
            originRt.capacity -= self.allNodes[B][1]
            targetRt.capacity += self.allNodes[B][1]
        self.SetTabuIterator(B, iterator)
        #self.sol.cost += rm.moveCost
    def FindBestSwapMove2(self, sm, iterator):
        profit = 0
        for firstRouteIndex in range(0, len(self.sol.routes)):
            rt1:Route = self.sol.routes[firstRouteIndex]
            for secondRouteIndex in range(firstRouteIndex, len(self.sol.routes)):
                rt2:Route = self.sol.routes[secondRouteIndex]
                for firstNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range(startOfSecondNodeIndex, len(rt2.sequenceOfNodes) - 1):

                        a1 = rt1.sequenceOfNodes[firstNodeIndex - 1]
                        b1 = rt1.sequenceOfNodes[firstNodeIndex]
                        c1 = rt1.sequenceOfNodes[firstNodeIndex + 1]

                        a2 = rt2.sequenceOfNodes[secondNodeIndex - 1]
                        b2 = rt2.sequenceOfNodes[secondNodeIndex]
                        c2 = rt2.sequenceOfNodes[secondNodeIndex + 1]

                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                costRemoved = math.dist(a1, b1) + math.dist(b1, b2) + math.dist(b2, c2)
                                costAdded = math.dist(a1, b2) + math.dist(b2, b1) + math.dist(b1, c2)
                                moveCost = costAdded - costRemoved
                            else:
                                costRemoved1 = math.dist(a1, b1) + math.dist(b1, c1)
                                costAdded1 = math.dist(a1, b2) + math.dist(b2, c1)
                                costRemoved2 = math.dist(a2, b2) + math.dist(b2, c2)
                                costAdded2 = math.dist(a2, b1) + math.dist(b1, c2)
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            new_route1 = []
                            for nodes in self.sol.routes[secondRouteIndex].sequenceOfNodes:
                                new_route1.append(nodes)
                            new_route1[firstNodeIndex] = b2
                            new_route1[secondNodeIndex] = b1
                            profit = self.CheckMaxProfit(new_route1, rt1.time + moveCost, rt1.capacity)
                        else:
                            if rt1.capacity - self.allNodes[b1][1] + self.allNodes[b2][1] > 150:
                                continue
                            if rt2.capacity - self.allNodes[b2][1] + self.allNodes[b1][1] > 150:
                                continue
                            costRemoved1 = math.dist(a1, b1) + math.dist(b1, c1)
                            costAdded1 = math.dist(a1, b2) + math.dist(b2, c1)
                            costRemoved2 = math.dist(a2, b2) + math.dist(b2, c2)
                            costAdded2 = math.dist(a2, b1) + math.dist(b1, c2)
                            costChangeFirstRoute = costAdded1 - costRemoved1 - self.allNodes[b1][2] + self.allNodes[b2][2]
                            costChangeSecondRoute = costAdded2 - costRemoved2 - self.allNodes[b2][2] + self.allNodes[b1][2]
                            if rt1.time + costChangeFirstRoute > 200:
                                continue
                            if rt2.time + costChangeSecondRoute > 200:
                                continue
                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            new_route1 = []
                            for nodes in rt1.sequenceOfNodes:
                                new_route1.append(nodes)
                            new_route2 = []
                            for nodes in rt2.sequenceOfNodes:
                                new_route2.append(nodes)
                            new_route1[firstNodeIndex] = b2
                            new_route2[secondNodeIndex] = b1
                            profit1 = self.CheckMaxProfit(new_route1, rt1.time + costChangeFirstRoute, rt1.capacity - self.allNodes[b1][1] + self.allNodes[b2][1])
                            profit2 = self.CheckMaxProfit(new_route2, rt2.time + costChangeSecondRoute, rt2.capacity - self.allNodes[b2][1] + self.allNodes[b1][1])
                            if profit1 > profit2:
                                profit = profit1
                            else:
                                profit = profit2
                        if self.MoveIsTabu(b1, iterator, profit) or self.MoveIsTabu(b2, iterator, profit):
                            continue

                        if profit + ((-1) * moveCost/4) > sm.profit:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm,profit + ((-1) * moveCost/4))
    def StoreBestSwapMove(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm, profit ):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.moveCost = moveCost
        sm.profit = profit
    def ApplySwapMove2(self, sm, iterator):
        rt1 = self.sol.routes[sm.positionOfFirstRoute]
        rt2 = self.sol.routes[sm.positionOfSecondRoute]
        b1 = rt1.sequenceOfNodes[sm.positionOfFirstNode]
        b2 = rt2.sequenceOfNodes[sm.positionOfSecondNode]
        rt1.sequenceOfNodes[sm.positionOfFirstNode] = b2
        rt2.sequenceOfNodes[sm.positionOfSecondNode] = b1

        if (rt1 == rt2):
            rt1.time += sm.moveCost
        else:
            rt1.time += sm.costChangeFirstRt
            rt2.time += sm.costChangeSecondRt
            rt1.capacity = rt1.capacity - self.allNodes[b1][1] + self.allNodes[b2][1]
            rt2.capacity = rt2.capacity + self.allNodes[b1][1] - self.allNodes[b2][1]
        self.SetTabuIterator(b1, iterator)
        self.SetTabuIterator(b2, iterator)
    def FindBestTwoOptMove2(self, top, iterator):
        for rtInd1 in range(0, len(self.sol.routes)):
            rt1:Route = self.sol.routes[rtInd1]
            for rtInd2 in range(rtInd1, len(self.sol.routes)):
                rt2:Route = self.sol.routes[rtInd2]
                for nodeInd1 in range(0, len(rt1.sequenceOfNodes) - 1):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 1):
                        moveCost = 10 ** 9
                        A = rt1.sequenceOfNodes[nodeInd1]
                        B = rt1.sequenceOfNodes[nodeInd1 + 1]
                        K = rt2.sequenceOfNodes[nodeInd2]
                        L = rt2.sequenceOfNodes[nodeInd2 + 1]

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.sequenceOfNodes) - 2:
                                continue
                            costAdded = math.dist(A, K) + math.dist(B, L)
                            costRemoved = math.dist(A, B) + math.dist(K, L)
                            moveCost = costAdded - costRemoved
                            rt1_new = []
                            for node in rt1.sequenceOfNodes:
                                rt1_new.append(node)
                            reversedSegment = reversed(
                                rt1_new[nodeInd1 + 1: nodeInd2 + 1])

                            rt1_new[nodeInd1 + 1: nodeInd2 + 1] = reversedSegment
                            profit = self.CheckMaxProfit(rt1_new, rt1.time + moveCost, rt1.capacity)
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.sequenceOfNodes) - 2 and nodeInd2 == len(rt2.sequenceOfNodes) - 2:
                                continue
                            costAdded = math.dist(A, L) + math.dist(B, K)
                            costRemoved = math.dist(A, B) + math.dist(K, L)
                            moveCost = costAdded - costRemoved
                            rt1_new = []
                            for i in rt1.sequenceOfNodes:
                                rt1_new.append(i)
                            rt2_new = []
                            for i in rt2.sequenceOfNodes:
                                rt2_new.append(i)
                            relocatedSegmentOfRt1 = rt1_new[nodeInd1 + 1:]

                            relocatedSegmentOfRt2 = rt2_new[nodeInd2 + 1:]

                            del rt1_new[nodeInd1 + 1:]
                            del rt2_new[nodeInd2 + 1:]

                            rt1_new.extend(relocatedSegmentOfRt2)
                            rt2_new.extend(relocatedSegmentOfRt1)

                            rt1_capacity = self.CapacityIsViolated(rt1_new)
                            if rt1_capacity > 150:
                                continue
                            rt2_capacity = self.CapacityIsViolated(rt2_new)
                            if rt2_capacity > 150:
                                continue
                            rt1_time = self.CalculateCost(rt1_new)
                            if rt1_time > 200:
                                continue
                            rt2_time = self.CalculateCost(rt2_new)
                            if rt2_time > 200:
                                continue
                            profit1 = self.CheckMaxProfit(rt1_new, rt1_time, rt1_capacity)
                            profit2 = self.CheckMaxProfit(rt2_new, rt2_time, rt2_capacity)
                            if profit1 > profit2:
                                profit = profit1
                            else:
                                profit = profit2
                        if self.MoveIsTabu(A, iterator, profit) or self.MoveIsTabu(K, iterator, profit):
                            continue

                        if profit + ((-1) * moveCost/4) > top.profit:
                            self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top, profit + ((-1) * moveCost/4))
    def CapacityIsViolated(self, route):
        load = 0
        for i in route:
            load += self.allNodes[i][1]
        return load
    def StoreBestTwoOptMove(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top, profit):
        top.positionOfFirstRoute = rtInd1
        top.positionOfSecondRoute = rtInd2
        top.positionOfFirstNode = nodeInd1
        top.positionOfSecondNode = nodeInd2
        top.moveCost = moveCost
        top.profit = profit
    def ApplyTwoOptMove2(self, top, iterator):
        rt1:Route = self.sol.routes[top.positionOfFirstRoute]
        rt2:Route = self.sol.routes[top.positionOfSecondRoute]
        rt1_problem = copy.copy(rt1)
        rt2_problem = copy.copy(rt2)
        if rt1 == rt2:
            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            #lst = list(reversedSegment)
            #lst2 = list(reversedSegment)
            rt1.sequenceOfNodes[top.positionOfFirstNode + 1 : top.positionOfSecondNode + 1] = reversedSegment
            self.SetTabuIterator(rt1.sequenceOfNodes[top.positionOfFirstNode], iterator)
            self.SetTabuIterator(rt1.sequenceOfNodes[top.positionOfSecondNode], iterator)
            #reversedSegmentList = list(reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1]))
            #rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegmentList

            rt1.time += top.moveCost

        else:
            #slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt1 = rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]

            #slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt2 = rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            del rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]
            del rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            rt1.sequenceOfNodes.extend(relocatedSegmentOfRt2)
            rt2.sequenceOfNodes.extend(relocatedSegmentOfRt1)

            self.SetTabuIterator(rt1.sequenceOfNodes[top.positionOfFirstNode], iterator)
            self.SetTabuIterator(rt2.sequenceOfNodes[top.positionOfSecondNode], iterator)


            self.UpdateRouteCostAndLoad(rt1)
            self.UpdateRouteCostAndLoad(rt2)
    def CalculateCost(self, route):
        tc = 0
        for i in range(0, len(route) - 1):
            A = route[i]
            B = route[i + 1]
            tc += math.dist(A, B) + self.allNodes[A][2]
        return tc
    def UpdateRouteCostAndLoad(self, rt: Route):
        tc = 0
        tl = 0
        for i in range(0, len(rt.sequenceOfNodes) - 1):
            A = rt.sequenceOfNodes[i]
            B = rt.sequenceOfNodes[i+1]
            tc += math.dist(A, B) + self.allNodes[A][2]
            tl += self.allNodes[A][1]
        rt.capacity = tl
        rt.time = tc
    def TestSolution(self, rt):
        rtCost = 0
        rtLoad = 0
        flag = False
        for i in range(0, len(rt) - 1):
            A = rt[i]
            B = rt[i + 1]
            rtCost += math.dist(A, B) + self.allNodes[A][2]
            rtLoad += self.allNodes[A][1]
        if rtCost > 200:
            flag = True
        if rtLoad > 150:
            flag = True
        return flag
    def CheckMaxProfit(self, routes, time, capacity):
        bestInsertion2 = CustomerInsertionAllPositions()
        flag = False
        profit = 0
        for key, values in self.allNodes.items():
            node = key
            if (key[0], key[1]) not in self.sol.visited:
                if capacity + self.allNodes[(node)][1] <= 150:
                    for j in range(0, len(routes) - 1):
                        A = routes[j]
                        B = routes[j + 1]
                        costAdded = math.dist(A, node) + math.dist(B, node)
                        costRemoved = math.dist(A, B)
                        trialCost = costAdded - costRemoved
                        if time + self.allNodes[node][2] + trialCost <= 200:
                            flag = True
                            if self.allNodes[node][3] > profit:
                                profit = self.allNodes[node][3]
                                bestInsertion2.customer = node
        return profit
    def ApplyCustomerInsertionAllPositions2(self, insertion, solution, rcl2):
        tup_index = random.randint(0, len(rcl2) - 1)
        tpl = rcl2[tup_index]
        node = tpl[1].customer
        rt = tpl[1].route
        # before the second depot occurrence
        insIndex = tpl[1].insertionPosition
        rt.sequenceOfNodes.insert(insIndex + 1, node)
        rt.time = rt.time + self.allNodes[node][2] + tpl[1].dz
        rt.capacity = rt.capacity + self.allNodes[node][1]
        solution.profit += self.allNodes[node][3]
        self.sol.visited.add(node)
    def MinimumInsertions2(self, solution):
        rcl2 = []
        bestInsertionProfit = CustomerInsertionAllPositions()
        flag = False
        count = 0
        for key, values in self.allNodes.items():
            if (key[0], key[1]) not in self.sol.visited:
                for route in self.sol.routes:
                    flag = self.IdentifyBestInsertionAllPositions2(bestInsertionProfit, route, (key[0], key[1]), rcl2)
                    if flag == True:
                        count = count + 1
        if count > 0:
            flag = True
            self.ApplyCustomerInsertionAllPositions2(bestInsertionProfit, solution, rcl2)
        return flag
    def IdentifyBestInsertionAllPositions2(self, bestInsertion, rt, node, rcl2):
        flag = False
        if rt.capacity + self.allNodes[(node)][1] <= 150:
            for j in range(0, len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[j]
                B = rt.sequenceOfNodes[j + 1]
                costAdded = math.dist(A, node) + math.dist(B, node)
                costRemoved = math.dist(A, B)
                trialCost = costAdded - costRemoved

                if rt.time + self.allNodes[node][2] + trialCost <= 200:
                    flag = True
                    if len(rcl2) < self.rcl_size2:
                        bestInsertion.profit = self.allNodes[node][3]
                        bestInsertion.dz = trialCost
                        bestInsertion.route = rt
                        bestInsertion.customer = node
                        bestInsertion.insertionPosition = j
                        new_tup = (self.allNodes[node][3], bestInsertion)
                        rcl2.append(new_tup)
                        rcl2.sort(key=lambda x: x[0], reverse=True)
                    elif self.allNodes[node][3] > rcl2[-1][0]:
                        rcl2.pop(len(rcl2) - 1)
                        bestInsertion.profit = self.allNodes[node][3]
                        bestInsertion.dz = trialCost
                        bestInsertion.route = rt
                        bestInsertion.customer = node
                        bestInsertion.insertionPosition = j
                        new_tup = (self.allNodes[node][3], bestInsertion)
                        rcl2.append(new_tup)
                        rcl2.sort(key=lambda x: x[0], reverse=True)
        return flag
    def CalculateTotalCostAndCapacity(self):
        flag = True
        for i in range(0, len(self.sol.routes)):
            c = 0
            l = 0
            rt = self.sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes) - 1):
                a = rt.sequenceOfNodes[j]
                b = rt.sequenceOfNodes[j + 1]
                c += math.dist(a, b) + self.allNodes[a][2]
                l += self.allNodes[a][1]
            if c > 200:
                flag = False
            if l > 150:
                flag = False
        return flag
    def FindeBestExchangeMove(self, ex):
        #για κάθε κόμβο που δεν έχει χρησιμοποιηθεί
        profit = 0
        for key, values in self.allNodes.items():
            if key not in self.sol.visited:
                #για κάθε διαδροή
                for RouteIndex in range(0, len(self.sol.routes)):
                    rt1: Route = self.sol.routes[RouteIndex]
                    #για κάθε κόμβο
                    for NodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                        A = rt1.sequenceOfNodes[NodeIndex - 1]
                        B = rt1.sequenceOfNodes[NodeIndex]
                        C = rt1.sequenceOfNodes[NodeIndex + 1]
                        moveCost = 10 ** 9
                        costRemoved = math.dist(A, B) + math.dist(B, C)
                        costAdded = math.dist(A, key) + math.dist(B, key)
                        moveCost = costAdded - costRemoved - self.allNodes[B][2] + self.allNodes[key][2]
                        if rt1.capacity + self.allNodes[key][1] - self.allNodes[B][1] > 150:
                            continue
                        if rt1.time + moveCost > 200:
                            continue
                        new_route1 = []
                        for i in rt1.sequenceOfNodes:
                            new_route1.append(i)
                        new_route1[NodeIndex] = key
                        if moveCost < 0:
                            profit = self.CheckMaxProfit(new_route1, rt1.time + moveCost , rt1.capacity + self.allNodes[key][1] - self.allNodes[B][1])
                        if profit > ex.profit:
                            self.StoreBestExchangeMove(RouteIndex, NodeIndex, moveCost, profit, key)
        print(profit)
    def StoreBestExchangeMove(self, RouteIndex, NodeIndex, moveCost, profit, key):
        self.positionOfRoute = RouteIndex
        self.positionOfNode = NodeIndex
        self.moveCost = moveCost
        self.profit = profit
        self.node = key
    def ApplyBestExchangeMove(self, ex):
        rt1 = self.sol.routes[ex.positionOfRoute]
        b1 = rt1.sequenceOfNodes[ex.positionOfNode]
        rt1.sequenceOfNodes[ex.positionOfFNode] = ex.node
        rt1.time += ex.moveCost
        rt1.capacity = rt1.capacity + self.allNodes[ex.node][1] - self.allNodes[b1][1]
    def Exchange(self):
        #για κάθε κόμβο που δεν έχει χρησιμοποιηθεί
        profit = 0
        insertion = None
        kerdos = -1
        flag = False
        for key, values in self.allNodes.items():
            if key not in self.sol.visited:
                #για κάθε διαδροή
                for RouteIndex in range(0, len(self.sol.routes)):
                    rt1: Route = self.sol.routes[RouteIndex]
                    #για κάθε κόμβο
                    for NodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                        A = rt1.sequenceOfNodes[NodeIndex - 1]
                        B = rt1.sequenceOfNodes[NodeIndex]
                        C = rt1.sequenceOfNodes[NodeIndex + 1]
                        moveCost = 10 ** 9
                        costRemoved = math.dist(A, B) + math.dist(B, C)
                        costAdded = math.dist(A, key) + math.dist(C, key)
                        moveCost = costAdded - costRemoved - self.allNodes[B][2] + self.allNodes[key][2]
                        if rt1.capacity + self.allNodes[key][1] - self.allNodes[B][1] > 150:
                            continue
                        if rt1.time + moveCost > 200 - 0.001:
                            continue
                        if moveCost < 0 and self.allNodes[key][3] > self.allNodes[B][3]:
                            flag = True
                            if kerdos == -1:
                                insertion = (self.allNodes[key][3], B, key, moveCost, rt1, NodeIndex)
                            else:
                                if insertion[0] < self.allNodes[key][3]:
                                    insertion = (self.allNodes[key][3], B, key, moveCost, rt1, NodeIndex)
        if flag == True:
            insertion[4].capacity = insertion[4].capacity + self.allNodes[insertion[2]][1] - self.allNodes[insertion[1]][1]
            insertion[4].time = insertion[4].time + insertion[3]
            self.sol.profit = self.sol.profit - self.allNodes[insertion[1]][3] + self.allNodes[insertion[2]][3]
            self.sol.visited.add(insertion[2])
            self.sol.visited.remove(insertion[1])
            insertion[4].sequenceOfNodes[insertion[5]] = insertion[2]
        return flag
    def SetTabuIterator(self, node, iterator):
        # n.isTabuTillIterator = iterator + self.tabuTenure
        #θέλω να είσαι ταμπού για τον αριθμό της επανάληψης συν κάποιον αριθμό
        self.sol.tabu[node] = iterator/9 + random.randint(1, 6)
    def MoveIsTabu(self, node, iterator, profit):
        if profit + self.sol.profit > self.bestSolution.profit - 0.001:
            return False
        if iterator < self.sol.tabu[node] and node != (23.142, 11.736):
            return True
        return False
    def FindBestRelocationMove(self, rm):
        profit = 0
        for originRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[originRouteIndex]
            for targetRouteIndex in range(0, len(self.sol.routes)):
                rt2: Route = self.sol.routes[targetRouteIndex]
                for originNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    for targetNodeIndex in range(0, len(rt2.sequenceOfNodes) - 1):

                        if originRouteIndex == targetRouteIndex and (
                                targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        if rt1 != rt2:
                            if rt2.capacity + self.allNodes[B][1] > 150:
                                continue
                        costAdded = math.dist(A, C) + math.dist(F, B) + math.dist(B, G)
                        costRemoved = math.dist(A, B) + math.dist(B, C) + math.dist(F, G)
                        originRtCostChange = math.dist(A, C) - math.dist(A, B) - math.dist(B, C) - self.allNodes[B][2]
                        targetRtCostChange = math.dist(F, B) + math.dist(B, G) - math.dist(F, G) + self.allNodes[B][2]
                        moveCost = costAdded - costRemoved
                        # ΣΤΟ ΜΟΥΒ ΚΟΣΤ ΥΠΟΛΟΓΙΣΕ ΚΑΙ ΤΟΥΣ ΧΡΟΝΟΥΣ ΕΞΥΠΗΡΕΤΗΣΕΙΣ ΩΣΤΕ ΝΑ ΕΙΝΑΙ ΑΡΝΗΤΙΚΟΙ
                        if rt1 != rt2:
                            if rt2.time + targetRtCostChange > 200:
                                continue
                        if rt1 == rt2:
                            if moveCost < 0:
                                new_route1 = []
                                for nodes in self.sol.routes[originRouteIndex].sequenceOfNodes:
                                    new_route1.append(nodes)
                                del new_route1[originNodeIndex]
                                if (originNodeIndex < targetNodeIndex):
                                    new_route1.insert(targetNodeIndex, B)
                                else:
                                    new_route1.insert(targetNodeIndex + 1, B)
                                profit = self.CheckMaxProfit(new_route1, rt1.time + moveCost,
                                                             self.sol.routes[originRouteIndex].capacity)

                        else:
                            if moveCost < 0:
                                new_route1 = []
                                new_route1 = rt1.sequenceOfNodes.copy()
                                del new_route1[originNodeIndex]
                                profit = self.CheckMaxProfit(new_route1, rt1.time + originRtCostChange,
                                                             rt1.capacity - self.allNodes[B][1])
                                new_route2 = []
                                new_route2 = rt2.sequenceOfNodes.copy()
                                new_route2.insert(targetNodeIndex + 1, B)
                                profit2 = self.CheckMaxProfit(new_route2, rt2.time + targetRtCostChange,
                                                              rt2.capacity + self.allNodes[B][1])
                                if profit2 > profit:
                                    profit = profit2
                        if (profit > rm.profit):
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                         targetNodeIndex, moveCost, originRtCostChange,
                                                         targetRtCostChange, rm, profit)
    def ApplyRelocationMove(self, rm: RelocationMove):
        originRt = self.sol.routes[rm.originRoutePosition]
        targetRt = self.sol.routes[rm.targetRoutePosition]

        B = originRt.sequenceOfNodes[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)

            originRt.time += rm.moveCost
        else:
            # (18.553, 6.847)
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.time += rm.costChangeOriginRt
            targetRt.time += rm.costChangeTargetRt
            originRt.capacity -= self.allNodes[B][1]
            targetRt.capacity += self.allNodes[B][1]
        # self.sol.cost += rm.moveCost
    def FindBestSwapMove(self, sm):
        profit = 0
        for firstRouteIndex in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[firstRouteIndex]
            for secondRouteIndex in range(firstRouteIndex, len(self.sol.routes)):
                rt2: Route = self.sol.routes[secondRouteIndex]
                for firstNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range(startOfSecondNodeIndex, len(rt2.sequenceOfNodes) - 1):

                        a1 = rt1.sequenceOfNodes[firstNodeIndex - 1]
                        b1 = rt1.sequenceOfNodes[firstNodeIndex]
                        c1 = rt1.sequenceOfNodes[firstNodeIndex + 1]

                        a2 = rt2.sequenceOfNodes[secondNodeIndex - 1]
                        b2 = rt2.sequenceOfNodes[secondNodeIndex]
                        c2 = rt2.sequenceOfNodes[secondNodeIndex + 1]

                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                costRemoved = math.dist(a1, b1) + math.dist(b1, b2) + math.dist(b2, c2)
                                costAdded = math.dist(a1, b2) + math.dist(b2, b1) + math.dist(b1, c2)
                                moveCost = costAdded - costRemoved
                            else:
                                costRemoved1 = math.dist(a1, b1) + math.dist(b1, c1)
                                costAdded1 = math.dist(a1, b2) + math.dist(b2, c1)
                                costRemoved2 = math.dist(a2, b2) + math.dist(b2, c2)
                                costAdded2 = math.dist(a2, b1) + math.dist(b1, c2)
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            new_route1 = []
                            for nodes in self.sol.routes[secondRouteIndex].sequenceOfNodes:
                                new_route1.append(nodes)
                            new_route1[firstNodeIndex] = b2
                            new_route1[secondNodeIndex] = b1
                            profit = self.CheckMaxProfit(new_route1, rt1.time + moveCost, rt1.capacity)
                        else:
                            if rt1.capacity - self.allNodes[b1][1] + self.allNodes[b2][1] > 150:
                                continue
                            if rt2.capacity - self.allNodes[b2][1] + self.allNodes[b1][1] > 150:
                                continue
                            costRemoved1 = math.dist(a1, b1) + math.dist(b1, c1)
                            costAdded1 = math.dist(a1, b2) + math.dist(b2, c1)
                            costRemoved2 = math.dist(a2, b2) + math.dist(b2, c2)
                            costAdded2 = math.dist(a2, b1) + math.dist(b1, c2)
                            costChangeFirstRoute = costAdded1 - costRemoved1 - self.allNodes[b1][2] + self.allNodes[b2][
                                2]
                            costChangeSecondRoute = costAdded2 - costRemoved2 - self.allNodes[b2][2] + \
                                                    self.allNodes[b1][2]
                            if rt1.time + costChangeFirstRoute > 200:
                                continue
                            if rt2.time + costChangeSecondRoute > 200:
                                continue
                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                            new_route1 = []
                            for nodes in rt1.sequenceOfNodes:
                                new_route1.append(nodes)
                            new_route2 = []
                            for nodes in rt2.sequenceOfNodes:
                                new_route2.append(nodes)
                            new_route1[firstNodeIndex] = b2
                            new_route2[secondNodeIndex] = b1
                            profit1 = self.CheckMaxProfit(new_route1, rt1.time + costChangeFirstRoute,
                                                          rt1.capacity - self.allNodes[b1][1] + self.allNodes[b2][1])
                            profit2 = self.CheckMaxProfit(new_route2, rt2.time + costChangeSecondRoute,
                                                          rt2.capacity - self.allNodes[b2][1] + self.allNodes[b1][1])
                            if profit1 > profit2:
                                profit = profit1
                            else:
                                profit = profit2
                        if profit > sm.profit:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex,
                                                   moveCost, costChangeFirstRoute, costChangeSecondRoute, sm, profit)
    def ApplySwapMove(self, sm):
        rt1 = self.sol.routes[sm.positionOfFirstRoute]
        rt2 = self.sol.routes[sm.positionOfSecondRoute]
        b1 = rt1.sequenceOfNodes[sm.positionOfFirstNode]
        b2 = rt2.sequenceOfNodes[sm.positionOfSecondNode]
        rt1.sequenceOfNodes[sm.positionOfFirstNode] = b2
        rt2.sequenceOfNodes[sm.positionOfSecondNode] = b1

        if (rt1 == rt2):
            rt1.time += sm.moveCost
        else:
            rt1.time += sm.costChangeFirstRt
            rt2.time += sm.costChangeSecondRt
            rt1.capacity = rt1.capacity - self.allNodes[b1][1] + self.allNodes[b2][1]
            rt2.capacity = rt2.capacity + self.allNodes[b1][1] - self.allNodes[b2][1]
    def FindBestTwoOptMove(self, top):
        for rtInd1 in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[rtInd1]
            for rtInd2 in range(rtInd1, len(self.sol.routes)):
                rt2: Route = self.sol.routes[rtInd2]
                for nodeInd1 in range(0, len(rt1.sequenceOfNodes) - 1):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 1):
                        moveCost = 10 ** 9
                        A = rt1.sequenceOfNodes[nodeInd1]
                        B = rt1.sequenceOfNodes[nodeInd1 + 1]
                        K = rt2.sequenceOfNodes[nodeInd2]
                        L = rt2.sequenceOfNodes[nodeInd2 + 1]

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.sequenceOfNodes) - 2:
                                continue
                            costAdded = math.dist(A, K) + math.dist(B, L)
                            costRemoved = math.dist(A, B) + math.dist(K, L)
                            moveCost = costAdded - costRemoved
                            rt1_new = []
                            for node in rt1.sequenceOfNodes:
                                rt1_new.append(node)
                            reversedSegment = reversed(
                                rt1_new[nodeInd1 + 1: nodeInd2 + 1])

                            rt1_new[nodeInd1 + 1: nodeInd2 + 1] = reversedSegment
                            profit = self.CheckMaxProfit(rt1_new, rt1.time + moveCost, rt1.capacity)
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.sequenceOfNodes) - 2 and nodeInd2 == len(rt2.sequenceOfNodes) - 2:
                                continue
                            costAdded = math.dist(A, L) + math.dist(B, K)
                            costRemoved = math.dist(A, B) + math.dist(K, L)
                            moveCost = costAdded - costRemoved
                            rt1_new = []
                            for i in rt1.sequenceOfNodes:
                                rt1_new.append(i)
                            rt2_new = []
                            for i in rt2.sequenceOfNodes:
                                rt2_new.append(i)
                            relocatedSegmentOfRt1 = rt1_new[nodeInd1 + 1:]

                            relocatedSegmentOfRt2 = rt2_new[nodeInd2 + 1:]

                            del rt1_new[nodeInd1 + 1:]
                            del rt2_new[nodeInd2 + 1:]

                            rt1_new.extend(relocatedSegmentOfRt2)
                            rt2_new.extend(relocatedSegmentOfRt1)

                            rt1_capacity = self.CapacityIsViolated(rt1_new)
                            if rt1_capacity > 150:
                                continue
                            rt2_capacity = self.CapacityIsViolated(rt2_new)
                            if rt2_capacity > 150:
                                continue
                            rt1_time = self.CalculateCost(rt1_new)
                            if rt1_time > 200:
                                continue
                            rt2_time = self.CalculateCost(rt2_new)
                            if rt2_time > 200:
                                continue
                            profit1 = self.CheckMaxProfit(rt1_new, rt1_time, rt1_capacity)
                            profit2 = self.CheckMaxProfit(rt2_new, rt2_time, rt2_capacity)
                            if profit1 > profit2:
                                profit = profit1
                            else:
                                profit = profit2

                        if profit > top.profit:
                            self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top, profit)
    def ApplyTwoOptMove(self, top):
        rt1: Route = self.sol.routes[top.positionOfFirstRoute]
        rt2: Route = self.sol.routes[top.positionOfSecondRoute]
        rt1_problem = copy.copy(rt1)
        rt2_problem = copy.copy(rt2)
        if rt1 == rt2:
            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            # lst = list(reversedSegment)
            # lst2 = list(reversedSegment)
            rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegment

            # reversedSegmentList = list(reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1]))
            # rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegmentList

            rt1.time += top.moveCost

        else:
            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt1 = rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]

            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt2 = rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            del rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]
            del rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            rt1.sequenceOfNodes.extend(relocatedSegmentOfRt2)
            rt2.sequenceOfNodes.extend(relocatedSegmentOfRt1)

            self.UpdateRouteCostAndLoad(rt1)
            self.UpdateRouteCostAndLoad(rt2)
