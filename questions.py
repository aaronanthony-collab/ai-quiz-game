"""
Question bank for the AI Quiz Arena (DSC401-6 Artificial Intelligence, Units I and II).

Every question is a plain Python dictionary with these keys:
    topic        - one of the syllabus topics listed in TOPICS
    type         - MCQ, True/False, Assertion-Reason, Fill in the Blank,
                   Match the Following, Scenario, Problem Solving
    level        - Easy, Medium or Hard
    question     - the question text
    options      - list of choices (for choice based questions)
    answer       - correct option text (choice questions) or list of accepted
                   answers (fill in the blank)
    pairs        - list of [left, right] pairs (match the following only)
    diagram      - optional text drawing / data shown in a code box
    hint         - shown when the player uses the Hint lifeline
    explanation  - shown after answering
    real_world   - True if the question is based on a real-world AI application
    search       - True if the question involves search / state-space problems
"""

TOPICS = [
    "Foundations and Applications of AI",
    "Turing Test",
    "Rational Agents",
    "Intelligent Agents",
    "Agents and Environments",
    "Good Behaviour",
    "Nature of Environments",
    "Problems and Problem Spaces",
    "State Space Search",
    "Production Systems",
    "Problem Characteristics",
    "Issues in Search Program Design",
    "Breadth First Search (BFS)",
    "Depth First Search (DFS)",
    "Iterative Deepening",
    "Hill Climbing and Variations",
    "Heuristic Search",
    "Best First Search",
    "Constraint Satisfaction Problems",
    "Means-End Analysis",
]

# The four standard options used in every Assertion-Reason question.
AR_OPTIONS = [
    "Both A and R are true, and R is the correct explanation of A",
    "Both A and R are true, but R is not the correct explanation of A",
    "A is true, but R is false",
    "A is false, but R is true",
]

# Text drawings reused by more than one question.
PUZZLE = """Start        Goal
2 8 3        1 2 3
1 6 4        8 _ 4
7 _ 5        7 6 5

(_ is the blank)"""

GRAPH_G1 = """Directed edges:
S -> A, S -> B
A -> C, A -> D
B -> D, B -> E
C -> G, D -> G, E -> G"""

GRAPH_ASTAR = """Edge costs:  S-A = 2,  S-B = 1,  A-G = 3,  B-G = 10
Heuristic h:  h(S) = 5,  h(A) = 3,  h(B) = 2,  h(G) = 0"""


QUESTIONS = [
    # ------------------------------------------------------------------
    # Foundations and Applications of AI
    # ------------------------------------------------------------------
    {
        "topic": "Foundations and Applications of AI",
        "type": "Fill in the Blank",
        "level": "Easy",
        "question": "Russell and Norvig describe four views of AI: thinking humanly, thinking rationally, "
                    "acting humanly and acting ______.",
        "answer": ["rationally", "rational"],
        "hint": "This is the rational agent approach.",
        "explanation": "The 'acting rationally' view, also called the rational agent approach, "
                       "is the one used in most modern AI.",
    },
    {
        "topic": "Foundations and Applications of AI",
        "type": "Scenario",
        "level": "Easy",
        "question": "A hospital installs software that studies chest X-ray images and marks areas that "
                    "may show pneumonia. Which AI application area is this?",
        "options": ["Computer vision", "Speech recognition", "Game playing", "Natural language generation"],
        "answer": "Computer vision",
        "hint": "The input to the system is an image.",
        "explanation": "Understanding the content of images is computer vision. Medical image analysis "
                       "is one of its most important applications.",
        "real_world": True,
    },
    {
        "topic": "Foundations and Applications of AI",
        "type": "Match the Following",
        "level": "Medium",
        "question": "Match each real-world AI application with the AI area it mainly belongs to.",
        "pairs": [
            ["Voice assistant such as Siri or Alexa", "Speech recognition and NLP"],
            ["Face unlock on a smartphone", "Computer vision"],
            ["Product suggestions on Amazon", "Machine learning (recommendation)"],
            ["Chess engine such as Deep Blue", "Search and game playing"],
        ],
        "hint": "Think about what kind of data each system works on.",
        "explanation": "Voice assistants work on speech and language, face unlock works on images, "
                       "recommendations learn from user data, and chess engines search through moves.",
        "real_world": True,
    },

    # ------------------------------------------------------------------
    # Turing Test
    # ------------------------------------------------------------------
    {
        "topic": "Turing Test",
        "type": "MCQ",
        "level": "Easy",
        "question": "Alan Turing proposed his famous test in a 1950 paper titled:",
        "options": ["Computing Machinery and Intelligence", "On Computable Numbers",
                    "A Logical Calculus of Ideas", "The Imitation of Life"],
        "answer": "Computing Machinery and Intelligence",
        "hint": "The paper starts with the question 'Can machines think?'",
        "explanation": "Turing published 'Computing Machinery and Intelligence' in 1950 and described "
                       "the imitation game, now called the Turing Test.",
    },
    {
        "topic": "Turing Test",
        "type": "True/False",
        "level": "Easy",
        "question": "In the Turing Test, the human interrogator can see both the machine and the human "
                    "they are questioning.",
        "options": ["True", "False"],
        "answer": "False",
        "hint": "Appearance should not give the machine away.",
        "explanation": "The interrogator is separated from both and communicates only through text, "
                       "so looks and voice cannot reveal which one is the machine.",
    },
    {
        "topic": "Turing Test",
        "type": "Assertion-Reason",
        "level": "Hard",
        "question": "Assertion (A): A machine that passes the Turing Test must have natural language "
                    "processing ability.\n\n"
                    "Reason (R): The interrogator talks to the machine only through a written text "
                    "conversation.",
        "options": AR_OPTIONS,
        "answer": AR_OPTIONS[0],
        "hint": "Ask yourself why the text-only setup forces the machine to handle language.",
        "explanation": "Since the whole test is a written conversation, the machine has to understand and "
                       "produce natural language. So R explains A.",
    },
    {
        "topic": "Turing Test",
        "type": "Scenario",
        "level": "Medium",
        "question": "A customer-support chatbot holds text conversations so well that most users believe "
                    "a human is typing the replies. Which idea does this relate to?",
        "options": ["The Turing Test (imitation game)", "Means-end analysis",
                    "Backtracking search", "Simulated annealing"],
        "answer": "The Turing Test (imitation game)",
        "hint": "The machine is judged by whether people can tell it apart from a human.",
        "explanation": "Judging a machine by whether a human can tell it apart from a person in conversation "
                       "is exactly the Turing Test idea.",
        "real_world": True,
    },

    # ------------------------------------------------------------------
    # Rational Agents
    # ------------------------------------------------------------------
    {
        "topic": "Rational Agents",
        "type": "MCQ",
        "level": "Easy",
        "question": "A rational agent is one that, for every possible percept sequence, selects the action that:",
        "options": ["Is expected to maximise its performance measure", "Is always the fastest",
                    "Copies human behaviour", "Uses the least memory"],
        "answer": "Is expected to maximise its performance measure",
        "hint": "Rationality is always judged against a performance measure.",
        "explanation": "A rational agent picks the action expected to maximise its performance measure, "
                       "given the evidence from the percept sequence and its built-in knowledge.",
    },
    {
        "topic": "Rational Agents",
        "type": "True/False",
        "level": "Medium",
        "question": "Rationality is the same as omniscience: a rational agent always knows the actual "
                    "outcome of its actions.",
        "options": ["True", "False"],
        "answer": "False",
        "hint": "Can anyone know the future outcome of every action?",
        "explanation": "Rationality maximises EXPECTED performance based on what the agent has perceived. "
                       "Omniscience would need knowledge of actual outcomes, which is impossible.",
    },
    {
        "topic": "Rational Agents",
        "type": "Fill in the Blank",
        "level": "Easy",
        "question": "PEAS stands for Performance measure, Environment, Actuators and ______.",
        "answer": ["sensors", "sensor"],
        "hint": "These are what the agent perceives with.",
        "explanation": "PEAS describes the task environment: Performance measure, Environment, "
                       "Actuators and Sensors.",
    },
    {
        "topic": "Rational Agents",
        "type": "Scenario",
        "level": "Medium",
        "question": "For a self-driving taxi, which of the following is an ACTUATOR?",
        "options": ["Steering, accelerator and brake", "Cameras and GPS",
                    "A safe and fast trip", "Roads, traffic and pedestrians"],
        "answer": "Steering, accelerator and brake",
        "hint": "Actuators are the parts the agent uses to act.",
        "explanation": "Steering, accelerator and brake are actuators. Cameras and GPS are sensors, "
                       "'safe and fast trip' is the performance measure, and roads and traffic are the environment.",
        "real_world": True,
    },

    # ------------------------------------------------------------------
    # Intelligent Agents
    # ------------------------------------------------------------------
    {
        "topic": "Intelligent Agents",
        "type": "Match the Following",
        "level": "Medium",
        "question": "Match each agent type with its description.",
        "pairs": [
            ["Simple reflex agent", "Acts on the current percept using condition-action rules"],
            ["Model-based reflex agent", "Keeps internal state to track parts of the world it cannot see"],
            ["Goal-based agent", "Chooses actions by searching or planning towards a goal"],
            ["Utility-based agent", "Compares how desirable different outcomes are when goals conflict"],
            ["Learning agent", "Improves its performance using a critic and a learning element"],
        ],
        "hint": "Go from the simplest agent to the most complex one.",
        "explanation": "These are the five basic agent types in increasing order of generality.",
    },
    {
        "topic": "Intelligent Agents",
        "type": "Scenario",
        "level": "Medium",
        "question": "A trip-planning app compares routes using travel time, toll cost and fuel use, and "
                    "picks the best trade-off. Which agent type is this?",
        "options": ["Utility-based agent", "Simple reflex agent", "Model-based reflex agent", "Table-driven agent"],
        "answer": "Utility-based agent",
        "hint": "Several conflicting factors are being weighed against each other.",
        "explanation": "When several goals or factors conflict and must be traded off, a utility function "
                       "scores each outcome. That is a utility-based agent.",
        "real_world": True,
    },
    {
        "topic": "Intelligent Agents",
        "type": "Assertion-Reason",
        "level": "Hard",
        "question": "Assertion (A): A simple reflex agent can get stuck in an infinite loop in a partially "
                    "observable environment.\n\n"
                    "Reason (R): It does not keep any internal state or percept history.",
        "options": AR_OPTIONS,
        "answer": AR_OPTIONS[0],
        "hint": "What can an agent do if it cannot remember what it did before?",
        "explanation": "Without memory, the same percept always gives the same action, so the agent can repeat "
                       "the same moves forever. R explains A.",
    },

    # ------------------------------------------------------------------
    # Agents and Environments
    # ------------------------------------------------------------------
    {
        "topic": "Agents and Environments",
        "type": "MCQ",
        "level": "Medium",
        "question": "Which statement correctly relates the agent function and the agent program?",
        "options": [
            "The agent function is an abstract mapping from percept sequences to actions; the agent program is its concrete implementation",
            "The agent program is an abstract mapping; the agent function is the code that implements it",
            "They are two names for exactly the same thing",
            "The agent function is the hardware; the agent program is the environment",
        ],
        "answer": "The agent function is an abstract mapping from percept sequences to actions; the agent program is its concrete implementation",
        "hint": "One is a mathematical idea, the other is actual code.",
        "explanation": "The agent function describes WHAT the agent does for every percept sequence. "
                       "The agent program is the code that runs on the architecture and implements it.",
    },
    {
        "topic": "Agents and Environments",
        "type": "Fill in the Blank",
        "level": "Easy",
        "question": "Agent = architecture + ______.",
        "answer": ["program", "agent program"],
        "hint": "The architecture is the hardware; this is the software part.",
        "explanation": "An agent is made of an architecture (the computing device with sensors and actuators) "
                       "plus an agent program that runs on it.",
    },
    {
        "topic": "Agents and Environments",
        "type": "True/False",
        "level": "Medium",
        "question": "A table-driven agent, which stores an action for every possible percept sequence, "
                    "is practical for large problems such as chess.",
        "options": ["True", "False"],
        "answer": "False",
        "hint": "Think about how many percept sequences there can be.",
        "explanation": "The table would have an astronomically large number of entries, so it cannot be built "
                       "or stored. Compact agent programs are needed instead.",
    },

    # ------------------------------------------------------------------
    # Good Behaviour
    # ------------------------------------------------------------------
    {
        "topic": "Good Behaviour",
        "type": "Scenario",
        "level": "Medium",
        "question": "A vacuum-cleaner robot is rewarded with one point for each unit of dirt it sucks up. "
                    "Which unwanted behaviour might this performance measure encourage?",
        "options": ["Dumping dirt on the floor and cleaning it again", "Switching itself off to save battery",
                    "Never leaving its charging dock", "Cleaning only squares that are already clean"],
        "answer": "Dumping dirt on the floor and cleaning it again",
        "hint": "How could the robot score more points without making the floor cleaner?",
        "explanation": "The robot could create dirt and clean it again to collect more points. "
                       "A better measure gives a point for each CLEAN square at each time step.",
        "real_world": True,
    },
    {
        "topic": "Good Behaviour",
        "type": "True/False",
        "level": "Easy",
        "question": "A performance measure should be designed according to what we actually want in the "
                    "environment, not according to how we think the agent should behave.",
        "options": ["True", "False"],
        "answer": "True",
        "hint": "Measure the result in the world, not the method.",
        "explanation": "Judging the outcome in the environment avoids rewarding the wrong behaviour.",
    },
    {
        "topic": "Good Behaviour",
        "type": "MCQ",
        "level": "Hard",
        "question": "Taking actions in order to change future percepts, such as looking both ways before "
                    "crossing a road, is called:",
        "options": ["Information gathering (exploration)", "Reflex action",
                    "Goal formulation", "Constraint propagation"],
        "answer": "Information gathering (exploration)",
        "hint": "The agent acts to learn more before the real decision.",
        "explanation": "A rational agent may need to gather information or explore. Looking before crossing "
                       "improves what the agent will perceive next.",
    },

    # ------------------------------------------------------------------
    # Nature of Environments
    # ------------------------------------------------------------------
    {
        "topic": "Nature of Environments",
        "type": "Match the Following",
        "level": "Medium",
        "question": "Match each environment property with its meaning.",
        "pairs": [
            ["Fully observable", "Sensors give access to the complete state at every time"],
            ["Deterministic", "The next state is completely determined by the current state and action"],
            ["Episodic", "Experience is divided into independent episodes"],
            ["Static", "The environment does not change while the agent is thinking"],
            ["Discrete", "A finite number of distinct states, percepts and actions"],
        ],
        "hint": "Match by the key word in each property name.",
        "explanation": "These are the standard properties used to classify task environments.",
    },
    {
        "topic": "Nature of Environments",
        "type": "MCQ",
        "level": "Hard",
        "question": "Which property does NOT describe the taxi-driving environment?",
        "options": ["Static", "Stochastic", "Dynamic", "Continuous"],
        "answer": "Static",
        "hint": "Traffic keeps moving while the taxi decides.",
        "explanation": "Taxi driving is partially observable, stochastic, sequential, dynamic, continuous "
                       "and multi-agent. It is NOT static because the world changes while the agent thinks.",
        "real_world": True,
    },
    {
        "topic": "Nature of Environments",
        "type": "Scenario",
        "level": "Easy",
        "question": "A machine on a factory line examines each part separately and labels it defective or "
                    "fine. The decision about one part never affects the next one. This environment is:",
        "options": ["Episodic", "Sequential", "Dynamic", "Continuous"],
        "answer": "Episodic",
        "hint": "Each decision is independent of the earlier ones.",
        "explanation": "When every decision is independent of past decisions, the environment is episodic. "
                       "Chess and taxi driving are sequential.",
        "real_world": True,
    },
    {
        "topic": "Nature of Environments",
        "type": "MCQ",
        "level": "Hard",
        "question": "Chess played with a clock is best classified as:",
        "options": [
            "Fully observable, deterministic, sequential, semi-dynamic, discrete, multi-agent",
            "Partially observable, stochastic, episodic, dynamic, continuous, single-agent",
            "Fully observable, stochastic, episodic, static, continuous, single-agent",
            "Partially observable, deterministic, episodic, static, discrete, multi-agent",
        ],
        "answer": "Fully observable, deterministic, sequential, semi-dynamic, discrete, multi-agent",
        "hint": "The whole board is visible, and the clock makes it semi-dynamic.",
        "explanation": "The board is fully visible, moves have fixed results, each move affects later ones, "
                       "the clock keeps running (semi-dynamic), there are finite moves, and there are two players.",
    },

    # ------------------------------------------------------------------
    # Problems and Problem Spaces
    # ------------------------------------------------------------------
    {
        "topic": "Problems and Problem Spaces",
        "type": "MCQ",
        "level": "Easy",
        "question": "Which of the following is NOT a component of a well-defined problem?",
        "options": ["Heuristic function", "Initial state", "Goal test", "Path cost"],
        "answer": "Heuristic function",
        "hint": "One of these is an optional extra used only in informed search.",
        "explanation": "A well-defined problem has an initial state, a set of actions (successor function), "
                       "a goal test and a path cost. A heuristic is only a helper for informed search.",
    },
    {
        "topic": "Problems and Problem Spaces",
        "type": "Problem Solving",
        "level": "Easy",
        "question": "In the 8-puzzle, how many different moves are possible from a state in which the "
                    "blank is in the centre square?",
        "options": ["4", "3", "2", "8"],
        "answer": "4",
        "hint": "The blank can move up, down, left or right.",
        "explanation": "A blank in the centre has four neighbouring squares, so there are 4 moves. "
                       "A corner blank has 2 moves and an edge blank has 3.",
        "search": True,
    },
    {
        "topic": "Problems and Problem Spaces",
        "type": "Problem Solving",
        "level": "Hard",
        "question": "There are 9! = 362,880 ways to arrange the tiles of the 8-puzzle, but only half of "
                    "them can be reached from any given start state. How many states are reachable?",
        "options": ["181,440", "362,880", "40,320", "9,000"],
        "answer": "181,440",
        "hint": "Divide 9! by 2.",
        "explanation": "Exactly half of the arrangements are reachable (parity argument): 362,880 / 2 = 181,440.",
        "search": True,
    },

    # ------------------------------------------------------------------
    # State Space Search
    # ------------------------------------------------------------------
    {
        "topic": "State Space Search",
        "type": "Problem Solving",
        "level": "Medium",
        "question": "Water jug problem: you have a 4-litre jug and a 3-litre jug with no markings, and a tap. "
                    "A state is (x, y) = litres in the 4 L and 3 L jugs. Starting from (0, 0), and counting each "
                    "fill, empty or pour as one step, what is the minimum number of steps to get exactly 2 litres "
                    "in the 4-litre jug?",
        "options": ["6", "4", "5", "8"],
        "answer": "6",
        "hint": "One path is (0,0) -> (0,3) -> (3,0) -> (3,3) -> (4,2) -> (0,2) -> (2,0).",
        "explanation": "BFS over the state space finds 6 steps: (0,0), (0,3), (3,0), (3,3), (4,2), (0,2), (2,0).",
        "search": True,
    },
    {
        "topic": "State Space Search",
        "type": "Problem Solving",
        "level": "Hard",
        "question": "Missionaries and cannibals: 3 missionaries and 3 cannibals must cross a river in a boat "
                    "that carries at most 2 people. Cannibals must never outnumber missionaries on a bank "
                    "where missionaries are present. What is the minimum number of river crossings?",
        "options": ["11", "9", "13", "7"],
        "answer": "11",
        "hint": "Represent a state as (missionaries on left, cannibals on left, boat side).",
        "explanation": "Searching the state space (M, C, boat side) with the safety rule gives a shortest "
                       "solution of 11 crossings.",
        "search": True,
    },
    {
        "topic": "State Space Search",
        "type": "Problem Solving",
        "level": "Medium",
        "question": "A complete search tree has a branching factor of 3 and a depth of 4 (the root is at "
                    "depth 0). How many nodes does the tree contain?",
        "options": ["121", "81", "120", "243"],
        "answer": "121",
        "hint": "Add the nodes at each level: 1 + 3 + 9 + ...",
        "explanation": "1 + 3 + 9 + 27 + 81 = 121 nodes.",
        "search": True,
    },

    # ------------------------------------------------------------------
    # Production Systems
    # ------------------------------------------------------------------
    {
        "topic": "Production Systems",
        "type": "MCQ",
        "level": "Easy",
        "question": "Which of the following is NOT a component of a production system?",
        "options": ["A neural network trainer", "A set of production rules",
                    "A global database (working memory)", "A control strategy"],
        "answer": "A neural network trainer",
        "hint": "A production system is built from rules, a database and a control strategy.",
        "explanation": "A production system has a set of rules, a global database and a control strategy "
                       "that decides which rule to apply next.",
    },
    {
        "topic": "Production Systems",
        "type": "True/False",
        "level": "Medium",
        "question": "In a monotonic production system, applying a rule never prevents the later application "
                    "of another rule that could have been applied earlier.",
        "options": ["True", "False"],
        "answer": "True",
        "hint": "Think of knowledge only growing and never being taken away.",
        "explanation": "That is the definition of a monotonic production system. Theorem proving is an example.",
    },
    {
        "topic": "Production Systems",
        "type": "MCQ",
        "level": "Medium",
        "question": "Which of the following is both monotonic and partially commutative?",
        "options": ["Theorem proving", "Chess", "Bridge", "Robot navigation"],
        "answer": "Theorem proving",
        "hint": "In this problem, facts once proved are never lost.",
        "explanation": "Theorem proving is monotonic and partially commutative (Rich and Knight). "
                       "Chess and Bridge are non-monotonic and not partially commutative, and robot "
                       "navigation is non-monotonic.",
    },
    {
        "topic": "Production Systems",
        "type": "Scenario",
        "level": "Medium",
        "question": "A medical expert system has rules such as 'IF fever AND cough THEN suspect flu' and a "
                    "working memory that holds the patient's symptoms. Which AI architecture is this?",
        "options": ["Production system", "Neural network", "Genetic algorithm", "Hill climbing"],
        "answer": "Production system",
        "hint": "IF-THEN rules plus a database of facts.",
        "explanation": "IF-THEN rules, a working memory and a control strategy that picks the next rule "
                       "make up a rule-based production system.",
        "real_world": True,
    },

    # ------------------------------------------------------------------
    # Problem Characteristics
    # ------------------------------------------------------------------
    {
        "topic": "Problem Characteristics",
        "type": "Match the Following",
        "level": "Medium",
        "question": "Match each problem with the characteristic it is a good example of.",
        "pairs": [
            ["Theorem proving", "Ignorable (steps can be ignored)"],
            ["8-puzzle", "Recoverable (steps can be undone)"],
            ["Chess", "Irrecoverable (moves cannot be undone)"],
            ["Symbolic integration", "Decomposable into smaller sub-problems"],
        ],
        "hint": "Ask: can a wrong step be ignored, undone, or never taken back?",
        "explanation": "These examples come from the standard list of problem characteristics.",
    },
    {
        "topic": "Problem Characteristics",
        "type": "MCQ",
        "level": "Medium",
        "question": "Which of these problems has a certain-outcome (predictable) universe, so a complete "
                    "plan can be made before acting?",
        "options": ["8-puzzle", "Bridge", "Controlling a robot in a crowded street", "Poker"],
        "answer": "8-puzzle",
        "hint": "Which one has no hidden cards and no random events?",
        "explanation": "In the 8-puzzle every move has a known result. In card games and crowded streets "
                       "the outcome is uncertain, so only partial plans are possible.",
    },
    {
        "topic": "Problem Characteristics",
        "type": "Fill in the Blank",
        "level": "Medium",
        "question": "A problem whose steps can be undone, such as the 8-puzzle, is called a ______ problem.",
        "answer": ["recoverable"],
        "hint": "Starts with 'r' and means 'can be recovered from'.",
        "explanation": "In a recoverable problem a wrong step can be backed out, so backtracking is possible.",
    },
    {
        "topic": "Problem Characteristics",
        "type": "Assertion-Reason",
        "level": "Hard",
        "question": "Assertion (A): The 8-puzzle is a recoverable problem.\n\n"
                    "Reason (R): The 8-puzzle has 181,440 reachable states.",
        "options": AR_OPTIONS,
        "answer": AR_OPTIONS[1],
        "hint": "Why can a wrong move in the 8-puzzle be fixed? Is it because of the number of states?",
        "explanation": "Both statements are true. The 8-puzzle is recoverable because every move can be undone "
                       "by moving the tile back. The number of states does not explain this, so R is not the reason for A.",
    },

    # ------------------------------------------------------------------
    # Issues in Search Program Design
    # ------------------------------------------------------------------
    {
        "topic": "Issues in Search Program Design",
        "type": "Fill in the Blank",
        "level": "Medium",
        "question": "Searching from the goal state back towards the initial state is called ______ reasoning.",
        "answer": ["backward", "backwards"],
        "hint": "The opposite of forward reasoning.",
        "explanation": "The direction of search (forward from the start or backward from the goal) is one "
                       "of the main design issues in search programs.",
    },
    {
        "topic": "Issues in Search Program Design",
        "type": "MCQ",
        "level": "Easy",
        "question": "Which change turns a search tree into a search graph and stops the same state from being "
                    "expanded again and again?",
        "options": ["Keeping a CLOSED list and checking new nodes against it", "Increasing the branching factor",
                    "Using a larger heuristic value", "Removing the goal test"],
        "answer": "Keeping a CLOSED list and checking new nodes against it",
        "hint": "Remember which nodes have already been expanded.",
        "explanation": "Checking each new node against the CLOSED list avoids repeated states, so the search "
                       "works on a graph instead of an ever-growing tree.",
    },
    {
        "topic": "Issues in Search Program Design",
        "type": "MCQ",
        "level": "Medium",
        "question": "When deciding whether to search forward from the initial state or backward from the goal, "
                    "which rule of thumb is used?",
        "options": ["Choose the direction in which the branching factor is smaller",
                    "Always search forward", "Always search backward",
                    "Choose the direction that has more rules"],
        "answer": "Choose the direction in which the branching factor is smaller",
        "hint": "A smaller branching factor means fewer nodes to explore.",
        "explanation": "Moving in the direction with fewer choices at each step keeps the search tree smaller. "
                       "If the start has fewer successors, go forward. If the goal has fewer predecessors, go backward.",
    },

    # ------------------------------------------------------------------
    # Breadth First Search
    # ------------------------------------------------------------------
    {
        "topic": "Breadth First Search (BFS)",
        "type": "MCQ",
        "level": "Easy",
        "question": "Which data structure does BFS use to hold the frontier?",
        "options": ["Queue (FIFO)", "Stack (LIFO)", "Priority queue ordered by h(n)", "Hash table only"],
        "answer": "Queue (FIFO)",
        "hint": "First in, first out.",
        "explanation": "BFS removes the oldest node first, so it explores level by level using a FIFO queue.",
    },
    {
        "topic": "Breadth First Search (BFS)",
        "type": "True/False",
        "level": "Medium",
        "question": "BFS is guaranteed to find the cheapest solution when all step costs are equal.",
        "options": ["True", "False"],
        "answer": "True",
        "hint": "BFS finds the shallowest goal first.",
        "explanation": "With equal step costs the shallowest goal is also the cheapest, and BFS reaches the "
                       "shallowest goal first, so it is optimal in that case.",
    },
    {
        "topic": "Breadth First Search (BFS)",
        "type": "Problem Solving",
        "level": "Medium",
        "question": "In the graph shown, BFS starts at S and visits neighbours in alphabetical order, "
                    "without revisiting nodes. In which order are the nodes visited?",
        "diagram": GRAPH_G1,
        "options": ["S, A, B, C, D, E, G", "S, A, C, G, D, B, E", "S, B, A, E, D, C, G", "S, A, B, D, C, E, G"],
        "answer": "S, A, B, C, D, E, G",
        "hint": "Finish all nodes at one depth before going deeper.",
        "explanation": "Depth 0: S. Depth 1: A, B. Depth 2: C, D, E. Depth 3: G.",
        "search": True,
    },
    {
        "topic": "Breadth First Search (BFS)",
        "type": "Scenario",
        "level": "Medium",
        "question": "To find the fewest connections between two people on a social network (degrees of "
                    "separation), which uninformed search algorithm fits best?",
        "options": ["BFS", "DFS", "Hill climbing", "Depth-limited search"],
        "answer": "BFS",
        "hint": "You want the shortest chain of friends.",
        "explanation": "BFS explores all people at distance 1, then 2, and so on, so the first time it "
                       "reaches the target it has found the shortest chain.",
        "real_world": True,
        "search": True,
    },

    # ------------------------------------------------------------------
    # Depth First Search
    # ------------------------------------------------------------------
    {
        "topic": "Depth First Search (DFS)",
        "type": "MCQ",
        "level": "Easy",
        "question": "DFS uses which data structure (directly, or through recursion)?",
        "options": ["Stack (LIFO)", "Queue (FIFO)", "Priority queue", "Heap ordered by f(n)"],
        "answer": "Stack (LIFO)",
        "hint": "Last in, first out.",
        "explanation": "DFS keeps going down the most recently generated node, which is stack behaviour.",
    },
    {
        "topic": "Depth First Search (DFS)",
        "type": "True/False",
        "level": "Medium",
        "question": "DFS is complete even when the state space is infinite.",
        "options": ["True", "False"],
        "answer": "False",
        "hint": "What if DFS goes down an endless path?",
        "explanation": "DFS can follow an infinitely deep branch and never come back, so it is not "
                       "complete in infinite spaces (or in graphs with loops, unless repeats are checked).",
    },
    {
        "topic": "Depth First Search (DFS)",
        "type": "Problem Solving",
        "level": "Hard",
        "question": "In the same graph, DFS (recursive) starts at S, visits neighbours in alphabetical order "
                    "and never revisits a node. In which order are the nodes visited?",
        "diagram": GRAPH_G1,
        "options": ["S, A, C, G, D, B, E", "S, A, B, C, D, E, G", "S, B, E, G, D, A, C", "S, A, D, G, C, B, E"],
        "answer": "S, A, C, G, D, B, E",
        "hint": "Go as deep as possible first: S -> A -> C -> G, then back up.",
        "explanation": "S, A, C, G (dead end), back to A then D (G already visited), back to S then B, "
                       "then E (G visited).",
        "search": True,
    },

    # ------------------------------------------------------------------
    # Iterative Deepening
    # ------------------------------------------------------------------
    {
        "topic": "Iterative Deepening",
        "type": "MCQ",
        "level": "Medium",
        "question": "Iterative deepening DFS combines:",
        "options": ["The completeness of BFS with the low memory use of DFS",
                    "The speed of greedy search with the optimality of A*",
                    "Hill climbing with random restarts",
                    "Forward and backward chaining"],
        "answer": "The completeness of BFS with the low memory use of DFS",
        "hint": "It runs DFS again and again with a growing depth limit.",
        "explanation": "IDDFS is complete (and optimal for equal step costs) like BFS, but needs only "
                       "O(bd) memory like DFS.",
    },
    {
        "topic": "Iterative Deepening",
        "type": "Problem Solving",
        "level": "Hard",
        "question": "A search tree has branching factor b = 2. Iterative deepening runs depth limits 0, 1, 2 "
                    "and 3. How many nodes are generated in total across all iterations (counting the root "
                    "each time)?",
        "options": ["26", "15", "31", "20"],
        "answer": "26",
        "hint": "A full binary tree of depth L has 2^(L+1) - 1 nodes.",
        "explanation": "Limit 0: 1 node. Limit 1: 3. Limit 2: 7. Limit 3: 15. Total = 1 + 3 + 7 + 15 = 26.",
        "search": True,
    },
    {
        "topic": "Iterative Deepening",
        "type": "Scenario",
        "level": "Medium",
        "question": "A chess program has a fixed time limit per move. It searches 1 move ahead, then 2, "
                    "then 3, and so on until time runs out, and plays the best move found so far. "
                    "Which technique is this?",
        "options": ["Iterative deepening", "Hill climbing", "Constraint propagation", "Means-end analysis"],
        "answer": "Iterative deepening",
        "hint": "The depth limit keeps increasing.",
        "explanation": "Increasing the search depth step by step, and always having a usable answer ready, "
                       "is how chess engines use iterative deepening.",
        "real_world": True,
    },

    # ------------------------------------------------------------------
    # Hill Climbing and Variations
    # ------------------------------------------------------------------
    {
        "topic": "Hill Climbing and Variations",
        "type": "MCQ",
        "level": "Medium",
        "question": "Which of these is NOT a known problem of hill climbing?",
        "options": ["Large memory use because the whole frontier is stored", "Local maxima",
                    "Plateaus", "Ridges"],
        "answer": "Large memory use because the whole frontier is stored",
        "hint": "Hill climbing only keeps the current state.",
        "explanation": "Hill climbing needs almost no memory. Its real problems are local maxima, "
                       "plateaus and ridges.",
    },
    {
        "topic": "Hill Climbing and Variations",
        "type": "Match the Following",
        "level": "Medium",
        "question": "Match each hill climbing variation with how it works.",
        "pairs": [
            ["Simple hill climbing", "Moves to the first neighbour that is better"],
            ["Steepest-ascent hill climbing", "Checks all neighbours and moves to the best one"],
            ["Stochastic hill climbing", "Picks randomly among the uphill neighbours"],
            ["Random-restart hill climbing", "Repeats the search from random starting states"],
            ["Simulated annealing", "Sometimes accepts downhill moves, less often over time"],
        ],
        "hint": "Look at how each method chooses its next move.",
        "explanation": "These variations try to reduce the problems of plain hill climbing.",
    },
    {
        "topic": "Hill Climbing and Variations",
        "type": "Assertion-Reason",
        "level": "Hard",
        "question": "Assertion (A): Hill climbing is guaranteed to find the global maximum.\n\n"
                    "Reason (R): Hill climbing always moves to a neighbouring state that has a better value.",
        "options": AR_OPTIONS,
        "answer": AR_OPTIONS[3],
        "hint": "Can moving only uphill ever trap you on a small hill?",
        "explanation": "R is true, because hill climbing only moves to better neighbours. But A is false: "
                       "this can end on a local maximum, a plateau or a ridge instead of the global maximum.",
    },
    {
        "topic": "Hill Climbing and Variations",
        "type": "Problem Solving",
        "level": "Hard",
        "question": "We are maximising a value. The current state has value 8 and its neighbours have values "
                    "6, 7, 8 and 5. What does steepest-ascent hill climbing do?",
        "options": ["Stops, because no neighbour is better than the current state",
                    "Moves to the neighbour with value 7",
                    "Moves to the neighbour with value 8",
                    "Moves to the neighbour with value 5"],
        "answer": "Stops, because no neighbour is better than the current state",
        "hint": "Is any neighbour strictly greater than 8?",
        "explanation": "The best neighbour (8) is not better than the current state (8), so the algorithm "
                       "stops. This is a local maximum or a flat plateau.",
        "search": True,
    },
    {
        "topic": "Hill Climbing and Variations",
        "type": "Scenario",
        "level": "Medium",
        "question": "A delivery company improves a route by repeatedly swapping two stops whenever the swap "
                    "shortens the total distance, and stops when no swap helps. Which method is this?",
        "options": ["Hill climbing (local search)", "Breadth first search", "Means-end analysis", "Minimax"],
        "answer": "Hill climbing (local search)",
        "hint": "It keeps making small improvements to one current solution.",
        "explanation": "Repeatedly making the best small improvement to the current solution is local search "
                       "by hill climbing. It may get stuck at a local optimum.",
        "real_world": True,
    },

    # ------------------------------------------------------------------
    # Heuristic Search
    # ------------------------------------------------------------------
    {
        "topic": "Heuristic Search",
        "type": "MCQ",
        "level": "Medium",
        "question": "A heuristic function is admissible if it:",
        "options": ["Never overestimates the true cost to reach the goal", "Always overestimates the cost",
                    "Is always equal to zero", "Is always a whole number"],
        "answer": "Never overestimates the true cost to reach the goal",
        "hint": "It must be optimistic.",
        "explanation": "An admissible heuristic is optimistic: h(n) is never greater than the real cheapest "
                       "cost from n to the goal. This keeps A* optimal.",
    },
    {
        "topic": "Heuristic Search",
        "type": "Problem Solving",
        "level": "Medium",
        "question": "For the 8-puzzle shown, how many tiles are misplaced compared with the goal "
                    "(not counting the blank)?",
        "diagram": PUZZLE,
        "options": ["4", "5", "3", "6"],
        "answer": "4",
        "hint": "Compare square by square. Tiles 2, 8, 1 and 6 are not in their goal squares.",
        "explanation": "Tiles 2, 8, 1 and 6 are in the wrong squares. Tiles 3, 4, 5 and 7 are correct, "
                       "so h1 = 4.",
        "search": True,
    },
    {
        "topic": "Heuristic Search",
        "type": "Problem Solving",
        "level": "Hard",
        "question": "For the same 8-puzzle, what is the Manhattan distance heuristic (sum of the horizontal "
                    "plus vertical distances of every tile from its goal square)?",
        "diagram": PUZZLE,
        "options": ["5", "4", "7", "6"],
        "answer": "5",
        "hint": "Tile 2 needs 1 move, tile 8 needs 2, tile 1 needs 1, tile 6 needs 1.",
        "explanation": "Tile 2: 1, tile 8: 2, tile 1: 1, tile 6: 1, others: 0. Total h2 = 5.",
        "search": True,
    },
    {
        "topic": "Heuristic Search",
        "type": "Scenario",
        "level": "Hard",
        "question": "Why is the straight-line (Euclidean) distance an admissible heuristic for finding road "
                    "routes between two cities?",
        "options": ["No road between two places can be shorter than the straight line, so it never overestimates",
                    "Roads are always straight",
                    "It is always larger than the real road distance",
                    "It ignores where the destination is"],
        "answer": "No road between two places can be shorter than the straight line, so it never overestimates",
        "hint": "Compare a straight line with a real winding road.",
        "explanation": "The straight line is the shortest possible path, so the real road distance is "
                       "always at least as long. Hence the heuristic never overestimates.",
        "real_world": True,
    },

    # ------------------------------------------------------------------
    # Best First Search
    # ------------------------------------------------------------------
    {
        "topic": "Best First Search",
        "type": "MCQ",
        "level": "Easy",
        "question": "A* search ranks the nodes in its OPEN list using f(n) =",
        "options": ["g(n) + h(n)", "h(n)", "g(n)", "g(n) - h(n)"],
        "answer": "g(n) + h(n)",
        "hint": "Cost so far plus estimated cost to go.",
        "explanation": "g(n) is the cost from the start to n and h(n) is the estimated cost from n to the goal. "
                       "A* expands the node with the lowest f(n).",
    },
    {
        "topic": "Best First Search",
        "type": "Problem Solving",
        "level": "Hard",
        "question": "For the graph and heuristic shown, which path and cost does A* return from S to G?",
        "diagram": GRAPH_ASTAR,
        "options": ["S-A-G, cost 5", "S-B-G, cost 11", "S-A-G, cost 8", "S-B-G, cost 3"],
        "answer": "S-A-G, cost 5",
        "hint": "Calculate f = g + h for A and B first.",
        "explanation": "f(A) = 2 + 3 = 5 and f(B) = 1 + 2 = 3, so B is expanded first and gives G with f = 11. "
                       "Then A (f = 5) is expanded and gives G with cost 5, which is cheaper. A* returns S-A-G, cost 5.",
        "search": True,
    },
    {
        "topic": "Best First Search",
        "type": "Problem Solving",
        "level": "Medium",
        "question": "For the same graph, which path and cost does GREEDY best-first search (using h(n) only) find?",
        "diagram": GRAPH_ASTAR,
        "options": ["S-B-G, cost 11", "S-A-G, cost 5", "S-A-G, cost 8", "S-B-G, cost 3"],
        "answer": "S-B-G, cost 11",
        "hint": "Greedy always picks the neighbour with the smaller h.",
        "explanation": "From S, h(B) = 2 is smaller than h(A) = 3, so greedy goes to B and then to G, "
                       "with cost 1 + 10 = 11. It misses the cheaper path through A.",
        "search": True,
    },
    {
        "topic": "Best First Search",
        "type": "True/False",
        "level": "Medium",
        "question": "Greedy best-first search is neither complete nor optimal in general.",
        "options": ["True", "False"],
        "answer": "True",
        "hint": "Think about the graph in the last question.",
        "explanation": "Greedy search can follow a misleading heuristic into dead ends or loops, and it "
                       "can return a path that is not the cheapest.",
    },
    {
        "topic": "Best First Search",
        "type": "Assertion-Reason",
        "level": "Hard",
        "question": "Assertion (A): A* search with an admissible heuristic returns an optimal solution.\n\n"
                    "Reason (R): An admissible heuristic never overestimates the true remaining cost, so a "
                    "cheaper path cannot be hidden behind a node with a wrongly high f value.",
        "options": AR_OPTIONS,
        "answer": AR_OPTIONS[0],
        "hint": "Why does it matter that the heuristic is optimistic?",
        "explanation": "Because h never overestimates, every node on an optimal path has f no larger than "
                       "the optimal cost, so A* expands it before accepting any worse goal. R explains A.",
    },

    # ------------------------------------------------------------------
    # Constraint Satisfaction Problems
    # ------------------------------------------------------------------
    {
        "topic": "Constraint Satisfaction Problems",
        "type": "Fill in the Blank",
        "level": "Easy",
        "question": "A constraint that involves exactly two variables is called a ______ constraint.",
        "answer": ["binary"],
        "hint": "One variable is unary, two variables is...",
        "explanation": "A unary constraint involves one variable, a binary constraint two, "
                       "and a global constraint many variables.",
    },
    {
        "topic": "Constraint Satisfaction Problems",
        "type": "Scenario",
        "level": "Medium",
        "question": "A college must schedule exams so that no student has two exams at the same time. "
                    "When this is modelled as a CSP, what are the available time slots?",
        "options": ["Domain values", "Variables", "Constraints", "Heuristics"],
        "answer": "Domain values",
        "hint": "The exams are the variables. What can each exam be assigned?",
        "explanation": "Variables = exams, domains = time slots, constraints = no clash for students "
                       "taking both exams.",
        "real_world": True,
    },
    {
        "topic": "Constraint Satisfaction Problems",
        "type": "MCQ",
        "level": "Medium",
        "question": "The MRV (minimum remaining values) heuristic chooses the next variable to assign as the one that:",
        "options": ["Has the fewest legal values left in its domain", "Has the most legal values left",
                    "Is involved in no constraints", "Was assigned most recently"],
        "answer": "Has the fewest legal values left in its domain",
        "hint": "Also called the 'fail-first' heuristic.",
        "explanation": "Choosing the most constrained variable first finds dead ends early and prunes "
                       "the search tree.",
    },
    {
        "topic": "Constraint Satisfaction Problems",
        "type": "Assertion-Reason",
        "level": "Hard",
        "question": "Assertion (A): Backtracking search can be used to solve a constraint satisfaction problem.\n\n"
                    "Reason (R): Backtracking assigns values to all the variables first and checks the constraints "
                    "only at the end.",
        "options": AR_OPTIONS,
        "answer": AR_OPTIONS[2],
        "hint": "When does backtracking check the constraints?",
        "explanation": "Backtracking assigns one variable at a time and checks the constraints after each assignment. "
                       "If a constraint is broken it goes back and tries another value. So A is true but R is false.",
    },
    {
        "topic": "Constraint Satisfaction Problems",
        "type": "Problem Solving",
        "level": "Hard",
        "question": "Modelled as a CSP with one queen in each column, how many distinct solutions does the "
                    "4-queens problem have on a 4 x 4 board?",
        "options": ["2", "1", "4", "8"],
        "answer": "2",
        "hint": "The two solutions are mirror images of each other.",
        "explanation": "Backtracking search finds exactly two solutions: rows (2, 4, 1, 3) and (3, 1, 4, 2).",
        "search": True,
    },
    {
        "topic": "Constraint Satisfaction Problems",
        "type": "MCQ",
        "level": "Medium",
        "question": "What is the minimum number of colours needed to colour the map of Australia "
                    "(WA, NT, SA, Q, NSW, V, T) so that no two neighbouring regions share a colour?",
        "options": ["3", "2", "4", "5"],
        "answer": "3",
        "hint": "WA, NT and SA all touch each other.",
        "explanation": "WA, NT and SA are mutually adjacent, so at least 3 colours are needed, and "
                       "3 colours are enough for the whole map.",
    },

    # ------------------------------------------------------------------
    # Means-End Analysis
    # ------------------------------------------------------------------
    {
        "topic": "Means-End Analysis",
        "type": "MCQ",
        "level": "Easy",
        "question": "Means-end analysis works by:",
        "options": ["Reducing the difference between the current state and the goal state step by step",
                    "Trying every possible state in turn",
                    "Always moving to the neighbour with the highest value",
                    "Colouring variables with the fewest colours"],
        "answer": "Reducing the difference between the current state and the goal state step by step",
        "hint": "It looks for the biggest difference and picks an operator to remove it.",
        "explanation": "MEA finds the difference between the current and goal states, then selects an "
                       "operator that reduces that difference.",
    },
    {
        "topic": "Means-End Analysis",
        "type": "Scenario",
        "level": "Medium",
        "question": "You are at home and must reach a city 1,000 km away. Using means-end analysis you choose "
                    "'take a flight' because it removes the biggest difference (distance). But a flight needs "
                    "you to be at the airport. What does means-end analysis do next?",
        "options": ["Sets a new sub-goal: get to the airport", "Gives up because the operator cannot be applied",
                    "Picks a random operator", "Restarts from the goal state"],
        "answer": "Sets a new sub-goal: get to the airport",
        "hint": "An unmet precondition becomes something to achieve first.",
        "explanation": "If the preconditions of the chosen operator are not met, MEA sets up a sub-goal to "
                       "satisfy them (reach the airport) and solves that first.",
        "real_world": True,
    },
    {
        "topic": "Means-End Analysis",
        "type": "True/False",
        "level": "Hard",
        "question": "Means-end analysis combines forward and backward reasoning, because the unmet "
                    "preconditions of an operator become sub-goals.",
        "options": ["True", "False"],
        "answer": "True",
        "hint": "Think about the airport example.",
        "explanation": "MEA works forward by applying operators and backward by creating sub-goals from "
                       "their preconditions. It was used in the General Problem Solver (GPS).",
    },
]


# Give every question an id, and fill in defaults so the app never has to check for missing keys.
for number, question in enumerate(QUESTIONS, start=1):
    question["id"] = number
    question.setdefault("options", [])
    question.setdefault("pairs", [])
    question.setdefault("diagram", "")
    question.setdefault("real_world", False)
    question.setdefault("search", False)
