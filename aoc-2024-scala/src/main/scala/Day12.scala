import scala.collection.mutable
import scala.io.Source

object Day12:
  type Point = (Int, Int)
  type Region = Set[Point]

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
        val region = bfs((r, c), visited, plant)
        regions(plant) = region :: regions(plant)

      regions.toMap

    def getPerimeterCells(region: Region): Set[Point] =
      val cells = mutable.Set[Point]()

      for
        (r, c) <- region
        (dr, dc) <- List((0, 1), (1, 0), (0, -1), (-1, 0))
        nr = r + dr
        nc = c + dc
        if nr < 0 || nr >= rows || nc < 0 || nc >= cols || !region.contains((nr, nc))
      do
        cells.add((r, c))

      cells.toSet

    def countCorners(region: Region): Int =
      val perimeterCells = getPerimeterCells(region)
      var corners = 0

      // For each perimeter cell, check if it forms a corner
      for (r, c) <- perimeterCells do
        val neighbors = List((0, 1), (1, 0), (0, -1), (-1, 0))
        val edgeDirections = neighbors.filter { (dr, dc) =>
          val nr = r + dr
          val nc = c + dc
          nr < 0 || nr >= rows || nc < 0 || nc >= cols || !region.contains((nr, nc))
        }

        // Count corners where we have exactly two non-opposite edges
        if edgeDirections.size == 2 then
          val (dr1, dc1) = edgeDirections(0)
          val (dr2, dc2) = edgeDirections(1)
          // Check if directions are not opposite (if sum of directions is not zero)
          if (dr1 + dr2 != 0 || dc1 + dc2 != 0) then
            corners += 1
        else if edgeDirections.size == 3 then
        // Three edges means two corners
          corners += 2
        else if edgeDirections.size == 4 then
        // Four edges means four corners (isolated cell)
          corners += 4

      corners

    def countSides(region: Region): Int =
      val corners = countCorners(region)
      // Number of sides equals number of corners in a closed polygon
      corners

    private def bfs(start: Point, visited: mutable.Set[Point], plant: Char): Region =
      val region = mutable.Set[Point]()
      val queue = mutable.Queue[Point](start)

      while queue.nonEmpty do
        val (r, c) = queue.dequeue()
        if !visited.contains((r, c)) then
          visited.add((r, c))
          region.add((r, c))

          for
            (nr, nc) <- getNeighbors(r, c)
            if grid(nr)(nc) == plant && !visited.contains((nr, nc))
          do
            queue.enqueue((nr, nc))

      region.toSet

    private def getNeighbors(r: Int, c: Int): List[Point] =
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
      val perimeterCells = garden.getPerimeterCells(region)
      val corners = garden.countCorners(region)
      val price = area * corners
      println(s"""Region of $plant plants:
                 |  Area: $area
                 |  Perimeter cells: ${perimeterCells.size}
                 |  Corners (sides): $corners
                 |  Price: $area * $corners = $price""".stripMargin)
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