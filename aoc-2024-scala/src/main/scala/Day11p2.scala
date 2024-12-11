object Day11p2:
  class StoneGraph:
    private val MaxSize = Math.pow(2, 75).toInt
    private val stones = new Array[Int](MaxSize)  // All stones
    private var currentSize = 0
    private var nextSize = 0
    private val tempArray = new Array[Int](MaxSize)

    private def transformStone(stone: Int): Unit =
      if stone == 0 then
        tempArray(nextSize) = 1
        nextSize += 1
      else
        // Search for this stone in previous generations
        var found = false
        var i = 0
        while i < currentSize && !found do
          if stones(i) == stone then
            found = true
            // Copy its children to temp array
            if i + 1 < currentSize then
              if stones(i + 1).toString.length % 2 == 0 then
                System.arraycopy(stones, i + 1, tempArray, nextSize, 2)
                nextSize += 2
              else
                System.arraycopy(stones, i + 1, tempArray, nextSize, 1)
                nextSize += 1
          i += 1

        if !found then
          val stoneStr = stone.toString
          if stoneStr.length % 2 == 0 then
            val mid = stoneStr.length / 2
            val left = stoneStr.take(mid).toInt
            val right = stoneStr.drop(mid).toInt
            tempArray(nextSize) = left
            tempArray(nextSize + 1) = right
            nextSize += 2
          else
            tempArray(nextSize) = stone * 2024
            nextSize += 1

    def growTree(): Unit =
      nextSize = 0
      var i = 0
      while i < currentSize do
        transformStone(stones(i))
        i += 1

      System.arraycopy(tempArray, 0, stones, 0, nextSize)
      currentSize = nextSize

    def initializeTree(initialStones: Array[Int]): Unit =
      System.arraycopy(initialStones, 0, stones, 0, initialStones.length)
      currentSize = initialStones.length

    def getSize: Int = currentSize

  def solvePuzzle(input: String, numBlinks: Int = 75): Int =
    val initialStones = input.trim.split("\\s+").map(_.toInt)
    val graph = StoneGraph()
    graph.initializeTree(initialStones)

    for blink <- 1 to numBlinks do
      graph.growTree()
      if blink % 10 == 0 then
        println(s"After $blink blinks: ${graph.getSize} stones")

    graph.getSize

  def solvePart2(input: String): Int = solvePuzzle(input, 75)

  def main(args: Array[String]): Unit =
    println("Day 11p2: Stone Transformation")

    // Test with example first
    val example = "125 17"
    val testCases = List(
      (6, 22),
      (25, 55312)
    )

    // Verify example cases
    for (blinks, expected) <- testCases do
      val result = Day11p2.solvePuzzle(example, blinks)
      assert(result == expected, s"After $blinks blinks: Expected $expected, got $result")
      println(s"Example after $blinks blinks: $result stones")

    println("\nRunning example for 75 blinks...")
    val exampleResult = Day11p2.solvePuzzle(example)
    println(s"Example result after 75 blinks: $exampleResult")

    try
      val input = scala.io.Source.fromFile(args(0)).mkString
      println("\nPart 2: 75 blinks")
      val part2Result = Day11p2.solvePart2(input)
      println(s"Number of stones after 75 blinks: $part2Result")
    catch
      case e: Exception =>
        println(s"Error reading input file: ${e.getMessage}")
        sys.exit(1)