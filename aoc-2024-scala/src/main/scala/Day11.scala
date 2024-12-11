object Day11:
  class StoneGraph:
    private var tree: List[Int] = Nil
    private val knownSubtrees = scala.collection.mutable.Map[Int, List[Int]]()

    private def transformStone(stone: Int): List[Int] =
      if stone == 0 then
        List(1)
      else
        val rez: Option[List[Int]] = knownSubtrees.get(stone)
        if rez.isDefined then
          return rez.get

        val stoneStr = stone.toString
        if stoneStr.length % 2 == 0 then
          val mid = stoneStr.length / 2
          val left = stoneStr.take(mid).toInt
          val right = stoneStr.drop(mid).toInt
          knownSubtrees.put(stone, List(left, right))
          List(left, right)
        else
          knownSubtrees.put(stone, List(stone * 2024))
          List(stone * 2024)

    def growTree(): Unit =
      tree = tree.flatMap { transformStone}

        // Get or create next level for each leaf

//        node =>
//          if knownSubtrees.contains(node) then
//          // Reuse known subtree for this value
//            knownSubtrees(node.value)
//          else
//            // Create new nodes for this value
//            val newNodes = transformStone(node.value).map(Node(_))
//            knownSubtrees(node.value) = newNodes
//            newNodes
//        }

    def initializeTree(stones: List[Int]): Unit =
      tree = stones

    def getLeafValues: List[Int] = tree

  def solvePuzzle(input: String, numBlinks: Int = 75): Int =
    val stones = input.trim.split("\\s+").map(_.toInt).toList
    val graph = StoneGraph()
    graph.initializeTree(stones)

    for blink <- 1 to numBlinks do
      graph.growTree()
      if blink % 10 == 0 then
        println(s"After $blink blinks: ${graph.getLeafValues.length} stones")

    graph.getLeafValues.length

  def solvePart1(input: String): Int = solvePuzzle(input, 25)
  def solvePart2(input: String): Int = solvePuzzle(input, 75)

  def main(args: Array[String]): Unit =
    println("Day 11: Stone Transformation")

    // Test with example first
    val example = "125 17"
    val testCases = List(
      (6, 22),
      (25, 55312)
    )

    // Verify example cases
    for (blinks, expected) <- testCases do
      val result = Day11.solvePuzzle(example, blinks)
      assert(result == expected, s"After $blinks blinks: Expected $expected, got $result")
      println(s"Example after $blinks blinks: $result stones")

    println("\nRunning example for 75 blinks...")
    val exampleResult = Day11.solvePuzzle(example)
    println(s"Example result after 75 blinks: $exampleResult")

    // Process actual input file
    try
      val input = scala.io.Source.fromFile(args(0)).mkString

//      println("\nPart 1: 25 blinks")
//      val part1Result = Day11.solvePart1(input)
//      println(s"Number of stones after 25 blinks: $part1Result")

      println("\nPart 2: 75 blinks")
      val part2Result = Day11.solvePart2(input)
      println(s"Number of stones after 75 blinks: $part2Result")

    catch
      case e: Exception =>
        println(s"Error reading input file: ${e.getMessage}")
        sys.exit(1)