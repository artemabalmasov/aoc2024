object Day10 {
  // Direction vectors for up, right, down, left
  val directions = List((-1, 0), (0, 1), (1, 0), (0, -1))

  def parseMap(input: String): Array[Array[Int]] = {
    input.trim.split("\n").map(_.trim.toCharArray.map(c => Option(c.asDigit).getOrElse(-1)))
  }

  def findTrailheads(grid: Array[Array[Int]]): List[(Int, Int)] = {
    val rows = grid.length
    val cols = grid(0).length
    (for {
      i <- 0 until rows
      j <- 0 until cols
      if grid(i)(j) == 0
    } yield (i, j)).toList
  }

  def isValid(pos: (Int, Int), grid: Array[Array[Int]]): Boolean = {
    val (row, col) = pos
    row >= 0 && row < grid.length && col >= 0 && col < grid(0).length
  }

  def findTrails(start: (Int, Int), grid: Array[Array[Int]]): Int = {
    def dfs(pos: (Int, Int), visited: List[(Int, Int)]): Set[(Int,Int)] = {
      val (row, col) = pos
      val currentHeight = grid(row)(col)

      if (currentHeight == 9) {
        // Found a valid endpoint
        //println((visited:+pos).map{case (r,c) => (r,c,grid(r)(c))})
        Set(pos)
      } else {
        var reachableNines: Set[(Int,Int)] = Set.empty[(Int, Int)]

        // Try all directions
        for {
          (dx, dy) <- directions
          newRow = row + dx
          newCol = col + dy
          newPos = (newRow, newCol)
          if isValid(newPos, grid) &&
            !visited.contains(newPos) &&
            grid(newRow)(newCol) == currentHeight + 1
        } {
          reachableNines = reachableNines ++ dfs(newPos, visited :+ pos)
        }

        reachableNines
      }
    }

    dfs(start, List.empty).size
  }

  def solve(input: String): Int = {
    val grid = parseMap(input)
    val trailheads = findTrailheads(grid)
//    println("zeros:")
//    println(trailheads.map{case (r,c) => (r,c,grid(r)(c))})
//    println("paths:")
    trailheads.map(start => findTrails(start, grid)).sum
  }

  def main(args: Array[String]): Unit = {
    // Test with the examples
    val example1 = """0123
                     |1234
                     |8765
                     |9876""".stripMargin

    val example2 = """...0...
                     |...1...
                     |...2...
                     |6543456
                     |7.....7
                     |8.....8
                     |9.....9""".stripMargin

    val example3 = """..90..9
                     |...1.98
                     |...2..7
                     |6543456
                     |765.987
                     |876....
                     |987....""".stripMargin

    val example4 = """89010123
                     |78121874
                     |87430965
                     |96549874
                     |45678903
                     |32019012
                     |01329801
                     |10456732""".stripMargin

    println(s"Example 1 result: ${solve(example1)}")
    println(s"Example 2 result: ${solve(example2)}")
    println(s"Example 3 result: ${solve(example3)}")
    val result4 = solve(example4)
    println(s"Example 4 result: $result4")
    assert(result4 == 36, s"Expected 36, got $result4")

    // Process actual input if provided
    if (args.nonEmpty) {
      val input = scala.io.Source.fromFile(args(0)).mkString
      val result = solve(input)
      println(s"Solution: $result")
    }
  }
}