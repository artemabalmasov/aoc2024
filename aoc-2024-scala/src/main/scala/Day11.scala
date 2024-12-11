object Day11:
  class StoneGraph:
    private var stones = Map.empty[BigInt, BigInt]  // Using BigInt for both keys and values

    private def transformStone(stone: BigInt): List[BigInt] =
      if stone == BigInt(0) then
        List(BigInt(1))
      else
        val stoneStr = stone.toString
        if stoneStr.length % 2 == 0 then
          val mid = stoneStr.length / 2
          val left = BigInt(stoneStr.take(mid))
          val right = BigInt(stoneStr.drop(mid))
          List(left, right)
        else
          List(stone * BigInt(2024))

    def printState(): Unit =
      println("Current stones and counts:")
      stones.toList.sortBy(_._1).foreach { case (stone, count) =>
        println(s"Stone $stone: $count times")
      }

    def growTree(): Unit =
      val newStones = stones.toList.flatMap { case (stone, count) =>
        transformStone(stone).map(_ -> count)
      }
      // Combine counts for same stones
      stones = newStones.groupMapReduce(_._1)(_._2)(_ + _)

    def initializeTree(initialStones: List[Int]): Unit =
      stones = initialStones.groupMapReduce(i => BigInt(i))(_ => BigInt(1))(_ + _)

    def getTotalStones: BigInt = stones.values.sum

  def solvePuzzle(input: String, numBlinks: Int = 75): BigInt =
    val stones = input.trim.split("\\s+").map(_.toInt).toList
    val graph = StoneGraph()
    graph.initializeTree(stones)

    println("Initial state:")
    graph.printState()

    for blink <- 1 to numBlinks do
      graph.growTree()
      if blink % 5 == 0 || blink == 1 then
        println(s"After $blink blinks: ${graph.getTotalStones} stones")
        graph.printState()

    graph.getTotalStones

  def solvePart1(input: String): BigInt = solvePuzzle(input, 25)
  def solvePart2(input: String): BigInt = solvePuzzle(input, 75)

  def main(args: Array[String]): Unit =
    println("Day 11: Stone Transformation")

    // Test with example first
    val example = "125 17"
    val testCases = List(
      (6, BigInt(22)),
      (25, BigInt(55312))
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

      println("\nPart 2: 75 blinks")
      val part2Result = Day11.solvePart2(input)
      println(s"Number of stones after 75 blinks: $part2Result")

    catch
      case e: Exception =>
        println(s"Error reading input file: ${e.getMessage}")
        sys.exit(1)