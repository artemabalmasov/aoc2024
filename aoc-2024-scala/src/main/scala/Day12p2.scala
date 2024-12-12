import scala.collection.mutable
import scala.io.Source

object Day12p2:
  type Point = (Int, Int)
  type Region = Set[Point]

  // Represents a fence at grid position (row, col)
  case class FencePoint(row: Int, col: Int, isHorizontal: Boolean):
    override def toString(): String = s"${if isHorizontal then "H" else "V"}($row,$col)"

  object FencePoint:
    given Ordering[FencePoint] = Ordering.by(f =>
      if f.isHorizontal then
        (f.isHorizontal, f.row, f.col) // Sort by col first for horizontal fences
      else
        (f.isHorizontal, f.col, f.row) // Sort by row first for vertical fences
    )

  class Garden(grid: Array[Array[Char]]):
    private val rows = grid.length
    private val cols = grid(0).length

    def findRegions(): Map[Char, List[Region]] =
      val visited = mutable.Set[Point]()
      val regions = mutable.Map[Char, List[Region]]().withDefaultValue(List())

      for
        r <- grid.indices
        c <- grid(0).indices
        if !visited.contains((r, c))
      do
        val plant = grid(r)(c)
        // Only use orthogonal connections in BFS
        val region = bfs((r, c), visited, plant)
        regions(plant) = region :: regions(plant)

      regions.toMap

    def getFences(region: Region): (Set[FencePoint], Set[FencePoint],Set[FencePoint], Set[FencePoint]) =
      val highFences = mutable.Set[FencePoint]()
      val lowFences = mutable.Set[FencePoint]()
      val leftFences = mutable.Set[FencePoint]()
      val rightFences = mutable.Set[FencePoint]()

      // Check each cell in region for fences needed
      for
        (r, c) <- region
      do
        // Check top fence
        if r == 0 || !region.contains((r-1, c)) then
          highFences.add(FencePoint(r, c, true))

        // Check bottom fence
        if r == rows-1 || !region.contains((r+1, c)) then
          lowFences.add(FencePoint(r+1, c, true))

        // Check left fence
        if c == 0 || !region.contains((r, c-1)) then
          leftFences.add(FencePoint(r, c, false))

        // Check right fence
        if c == cols-1 || !region.contains((r, c+1)) then
          rightFences.add(FencePoint(r, c+1, false))

      (highFences.toSet, lowFences.toSet,leftFences.toSet, rightFences.toSet)

    def countSides(region: Region): Int =
      val (highFences, lowFences, leftFences, rightFences) = getFences(region)

      // Print all fences by category
      println(
        s"""  High fences (${highFences.size}):
           |    ${highFences.toList.sorted.grouped(5).map(_.mkString(", ")).mkString("\n    ")}
           |  Low fences (${lowFences.size}):
           |    ${lowFences.toList.sorted.grouped(5).map(_.mkString(", ")).mkString("\n    ")}
           |  Left fences (${leftFences.size}):
           |    ${leftFences.toList.sorted.grouped(5).map(_.mkString(", ")).mkString("\n    ")}
           |  Right fences (${rightFences.size}):
           |    ${rightFences.toList.sorted.grouped(5).map(_.mkString(", ")).mkString("\n    ")}""".stripMargin)

      // Count high horizontal connected pieces
      val visitedHigh = mutable.Set[FencePoint]()
      var highPieces = 0

      for fence <- highFences.toList.sorted if !visitedHigh(fence) do
        var current = fence
        visitedHigh.add(current)
        var hasNext = true

        while hasNext do
          val next = FencePoint(current.row, current.col + 1, true)
          if highFences.contains(next) && !visitedHigh(next) then
            current = next
            visitedHigh.add(current)
          else
            hasNext = false

        highPieces += 1

      // Count low horizontal connected pieces
      val visitedLow = mutable.Set[FencePoint]()
      var lowPieces = 0

      for fence <- lowFences.toList.sorted if !visitedLow(fence) do
        var current = fence
        visitedLow.add(current)
        var hasNext = true

        while hasNext do
          val next = FencePoint(current.row, current.col + 1, true)
          if lowFences.contains(next) && !visitedLow(next) then
            current = next
            visitedLow.add(current)
          else
            hasNext = false

        lowPieces += 1

      // Count left vertical connected pieces
      val visitedLeft = mutable.Set[FencePoint]()
      var leftPieces = 0

      for fence <- leftFences.toList.sorted if !visitedLeft(fence) do
        var current = fence
        visitedLeft.add(current)
        var hasNext = true

        while hasNext do
          val next = FencePoint(current.row + 1, current.col, false)
          if leftFences.contains(next) && !visitedLeft(next) then
            current = next
            visitedLeft.add(current)
          else
            hasNext = false

        leftPieces += 1

      // Count right vertical connected pieces
      val visitedRight = mutable.Set[FencePoint]()
      var rightPieces = 0

      for fence <- rightFences.toList.sorted if !visitedRight(fence) do
        var current = fence
        visitedRight.add(current)
        var hasNext = true

        while hasNext do
          val next = FencePoint(current.row + 1, current.col, false)
          if rightFences.contains(next) && !visitedRight(next) then
            current = next
            visitedRight.add(current)
          else
            hasNext = false

        rightPieces += 1

      println(s"""  Pieces:
                 |    High: $highPieces
                 |    Low: $lowPieces
                 |    Left: $leftPieces
                 |    Right: $rightPieces
                 |    Total: ${highPieces + lowPieces + leftPieces + rightPieces}""".stripMargin)

      highPieces + lowPieces + leftPieces + rightPieces

    private def bfs(start: Point, visited: mutable.Set[Point], plant: Char): Region =
      val region = mutable.Set[Point]()
      val queue = mutable.Queue[Point](start)

      while queue.nonEmpty do
        val (r, c) = queue.dequeue()
        if !visited.contains((r, c)) && grid(r)(c) == plant then
          visited.add((r, c))
          region.add((r, c))

          // Only check orthogonal neighbors for connectivity
          for
            (nr, nc) <- getOrthogonalNeighbors(r, c)
            if grid(nr)(nc) == plant && !visited.contains((nr, nc))
          do
            queue.enqueue((nr, nc))

      region.toSet

    // Only get orthogonal (non-diagonal) neighbors
    private def getOrthogonalNeighbors(r: Int, c: Int): List[Point] =
      List((0, 1), (1, 0), (0, -1), (-1, 0)).flatMap { (dr, dc) =>
        val nr = r + dr
        val nc = c + dc
        if 0 <= nr && nr < rows && 0 <= nc && nc < cols then
          Some((nr, nc))
        else None
      }

  def solvePuzzle(input: String): Int =
    val garden = Garden(input.linesIterator.map(_.toCharArray).toArray)
    val regions = garden.findRegions()

    var totalPrice = 0
    for
      (plant, plantRegions) <- regions
      region <- plantRegions
    do
      val area = region.size
      val sides = garden.countSides(region)
      val price = area * sides
      println(s"""Region of $plant plants:
                 |  Area: $area
                 |  Continuous pieces (sides): $sides
                 |  Price: $area * $sides = $price""".stripMargin)
      totalPrice += price

    totalPrice

  def main(args: Array[String]): Unit =
    println("Day 12: Garden Regions - Part 2")

    val examples = List(
      """AAAA
        |BBCD
        |BBCC
        |EEEC""".stripMargin,
      """OOOOO
        |OXOXO
        |OOOOO
        |OXOXO
        |OOOOO""".stripMargin,
      """EEEEE
        |EXXXX
        |EEEEE
        |EXXXX
        |EEEEE""".stripMargin,
      """AAAAAA
        |AAABBA
        |AAABBA
        |ABBAAA
        |ABBAAA
        |AAAAAA""".stripMargin
    )

    val expectedResults = List(80, 436, 236, 368)

    examples.zip(expectedResults).zipWithIndex.foreach { case ((example, expected), i) =>
      println(s"\nTesting example ${i + 1}:")
      val result = solvePuzzle(example)
      assert(result == expected, s"Example ${i + 1}: Expected $expected, got $result")
      println(s"Example ${i + 1} result: $result")
    }

    if args.nonEmpty then
      try
        val input = Source.fromFile(args(0)).mkString
        val result = solvePuzzle(input)
        println(s"\nPuzzle result: $result")
      catch
        case e: Exception =>
          println(s"Error reading input file: ${e.getMessage}")
          sys.exit(1)