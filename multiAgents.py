# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # kiểm tra xem đã thắng hay chưa
        if successorGameState.isWin():
            return 10000

        # tìm thức ăn gần nhất
        closestFood = min([manhattanDistance(newPos,foodPos) for foodPos in newFood.asList()])

        # kiểm tra điều kiện nguy hiểm là ở gần ma khi ma không hoảng sợ
        for ghost in newGhostStates:
            if ghost.scaredTimer == 0 and manhattanDistance(newPos,ghost.getPosition()) < 2:
                return -10000
        #vì thức ăn gần nhất sẽ có điểm so sánh cao hơn nên sử dụng phép chia  
        return successorGameState.getScore() + 1.0/closestFood        

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        # choose là đường đi còn peak là điểm cần xét và kết quả trả về là choose 
        choose = None
        peak = -10000
        # duyệt hành động của pacman ở lúc khởi đầu
        for action in gameState.getLegalActions(0):
            # trạng thái của từng bước đi cần được lưu lại để sau gọi đệ quy cho từng node con phía sau để đưa ra phương án tối nhất
            state = gameState.generateSuccessor(0,action)
            # gán score là kết quả trả về sau khi tính toán theo lần đi của tác tử
            # ở đây mỗi lượt đi có thể lần đi của pacman hoặc ghost 
            # 1 == turn ở bên dưới là số lần đi đó
            score = self.min_Max(state,1)
            #trả về điểm tương ứng cùng với đường đi tới điểm đó
            if peak < score:
                peak = score
                choose = action
        return choose

    def min_Max(self,gameState,turn):
        # agentN là số tác tử có của trạn thái game
        agentN = gameState.getNumAgents()
        # agentIndex là số đại diện cho đó là pacman hay ghost với 0: pacman còn !0: ghost như gợi ý ở trên
        agentIndex = turn % agentN
        # độ sâu so với self.depth của đề bài là kết quả phần nguyên của turn chia cho số tác tử
        depth = turn // agentN
        # hàm được gọi đệ quy đến khi có kq của trờ chơi hoặc độ sâu của cây = độ sâu mà đề bài đưa
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        # gọi đệ quy với tác tử là pacman hoặc người cùng với độ sâu depth tăng dần 
        # values là mảng mà trong đó hàm đẹ quy được gọi để duyệt đến khi kết thúc hoặc đạt đến độ sâu cần thiết thì dừng
        values = [self.min_Max(gameState.generateSuccessor(agentIndex,action),turn+1) for action in gameState.getLegalActions(agentIndex)]
        # nếu agentIndex = 0 thì đó là pacman sẽ trả về điểm max(nước đi tốt nhất) và ngược lại là ma sẽ trả về nước đi tốt nhất với ma
        # tại thời điểm này thì với agentIndex đại diện cho pacman thì sẽ chọn kết quả tốt nhất là max 
        # còn với !0: ghost thì kết quả là xấu nhất với min
        if agentIndex == 0:
            return max(values)
        else:
            return min(values)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        # khởi tạo biến choose và peak như với minmax ở trên
        # ở đây thêm 2 biến alpha và belta để lưu 
        choose = None
        # peak là đỉnh cần xét,alpha đại diện tối ưu hiện tại của pacman,còn beta là đại diện cho tối ưu hiện tại của ghost
        # khi pacman cần tìm max thì khi ở 1 thời điểm mà nó lớn hơn tất cả con đã xét thì có thể loại bỏ cắt bỏ những con của chúng mà ko cần xét thêm nữa
        # tương tự với ghost cần tìm min có beta
        peak = -10000
        alpha = -10000
        beta = 10000
        for action in gameState.getLegalActions(0):
            state = gameState.generateSuccessor(0,action)
            score = self.AlphaBeta(state,1,alpha,beta)
            alpha = max(alpha, score)
            if peak < score:
                peak = score
                choose = action
        return choose

    def AlphaBeta(self,gameState,turn,alpha,beta):
        agentN = gameState.getNumAgents()
        agentIndex = turn % agentN
        depth = turn // agentN
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        # khởi tạo đỉnh hiện thời với agentIndex !=0
        peak = 10000 
        if agentIndex == 0:
            peak = -10000
        for action in gameState.getLegalActions(agentIndex):
            # gọi đệ quy tới các nodeCon
            value = self.AlphaBeta(gameState.generateSuccessor(agentIndex,action),turn+1,alpha,beta)
            # xét với pacman thì khi value > các giá trị tối đa đạt ra thì trả về 
            if agentIndex == 0:
                if value > beta:
                    return value
                #nếu không thì gán lại alpha= max lớn nhất của các nodecon và peak hiện thời là giá trị max của các node khi đã xét 
                else:    
                    alpha = max(alpha, value)
                    peak = max(peak,value)
            #xét với ghost thì cũng tương tự nhưng chiều thì ngược lại vì cần tìm node min 
            else:
                if value < alpha:
                    return value
                else:
                    beta = min(beta,value)
                    peak = min(peak,value)   
        return peak

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        # ở hàm expectimax thì cách viết giống với ở minimax 
        # điểm khác biệt ở chỗ là với minimax thì tác tử là ghost thì kết quả trả về sẽ là min
        # nhưng với expectimax thì ko phải lúc nào ghost cũng có lựa chọn tối ưu nhất 
        # nên ở hàm expectimax thì kết quả trả về sẽ là trung bình cộng của các trường hợp ghost có thể đi
        choose = None
        peak = -10000
        for action in gameState.getLegalActions(0):
            state = gameState.generateSuccessor(0,action)
            score = self.Expectimax(state,1)
            if peak < score:
                peak = score
                choose = action
        return choose

    def Expectimax(self,gameState,turn):
        # như giải thích phía trên nội dung hàm expectimax giống với minimax 
        # điểm khác biệt là kết quả trả về khi tác tử là ghost thì kết quả đó ko còn là min mà là trung bình của các nước đi có thể của ghost
        agentN = gameState.getNumAgents()
        agentIndex = turn % agentN
        depth = turn // agentN
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        values = [self.Expectimax(gameState.generateSuccessor(agentIndex,action),turn+1) for action in gameState.getLegalActions(agentIndex)]
        if agentIndex == 0:
            return max(values)
        # điểm khác biệt kết quả là trung bình cộng khi so với min của minimax
        return float(sum(values))/float(len(values))
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # vấn như hàm reflex nhưng giờ không cần xét vị trí con ma nữa mà chỉ xét khoảng cách gần nhất dựa theoe vị trí pacman hiện thời
    currentPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    if len(foods) != 0:
        closestFood = min(manhattanDistance(currentPos,food) for food in foods)
        return currentGameState.getScore() +1.0/closestFood
    else:
        return currentGameState.getScore()    
    


# Abbreviation
better = betterEvaluationFunction
