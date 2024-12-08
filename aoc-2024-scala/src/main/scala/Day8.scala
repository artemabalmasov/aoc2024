import scala.io.Source

object Day8:
  case class Antenna(sign: String) {
    private var coords: List[(Int, Int)] = List.empty
    def coordinates: List[(Int, Int)] = coords
    def add(row: Int, col: Int): Unit = {
      coords = (row, col) :: coords
    }
  }

  def readInput(filename: String): String = {
    val source = scala.io.Source.fromFile(filename)
    try source.mkString.trim
    finally source.close()
  }

  def parseMap(text: String): (Array[Array[Char]], Map[Char, Antenna]) = {
    val lines = text.trim.split("\n")
    val grid = lines.map(_.toCharArray)
    var antennas = Map.empty[Char, Antenna]

    for {
      row <- grid.indices
      col <- grid(row).indices
      char = grid(row)(col)
      if char != '.'
    } {
      val antenna = antennas.getOrElse(char, Antenna(char.toString))
      antenna.add(row, col)
      antennas = antennas + (char -> antenna)
    }

    (grid, antennas)
  }

  def arePointsCollinear(p1: (Int, Int), p2: (Int, Int), p3: (Int, Int)): Boolean = {
    val (x1, y1) = p1
    val (x2, y2) = p2
    val (x3, y3) = p3
    (y2 - y1) * (x3 - x2) == (y3 - y2) * (x2 - x1)
  }

  def normalizeDirection(dx: Int, dy: Int): (Int, Int) = {
    if (dx == 0 && dy == 0) (0, 0)
    else {
      val d = if (dx != 0 && dy != 0)
        gcd(math.abs(dx), math.abs(dy))
      else
        math.max(math.abs(dx), math.abs(dy))
      (dx / d, dy / d)
    }
  }

  def gcd(a: Int, b: Int): Int = {
    if (b == 0) math.abs(a)
    else gcd(b, a % b)
  }

  def findAllCollinearPoints(p1: (Int, Int), p2: (Int, Int), rows: Int, cols: Int): Set[(Int, Int)] = {
    val (x1, y1) = p1
    val (x2, y2) = p2

    val (dx, dy) = normalizeDirection(x2 - x1, y2 - y1)
    if ((dx, dy) == (0, 0)) return Set.empty

    val minX = 0
    val maxX = rows - 1
    val minY = 0
    val maxY = cols - 1

    val (tStart, tEnd) = if (dx != 0) {
      val tMinX = if (dx != 0) (minX - x1) / dx else Int.MaxValue
      val tMaxX = if (dx != 0) (maxX - x1) / dx else Int.MaxValue
      (math.min(tMinX, tMaxX), math.max(tMinX, tMaxX))
    } else {
      val tY = if (dy != 0) ((minY - y1) / dy, (maxY - y1) / dy) else (0, 0)
      tY
    }

    (tStart to tEnd).foldLeft(Set.empty[(Int, Int)]) { (points, t) =>
      val x = x1 + dx * t
      val y = y1 + dy * t
      if (0 <= x && x < rows && 0 <= y && y < cols)
        points + ((x, y))
      else
        points
    }
  }

  def findAntinodesPart1(grid: Array[Array[Char]], antennas: Map[Char, Antenna]): Set[(Int, Int)] = {
    val rows = grid.length
    val cols = grid(0).length

    val antinodes = for {
      (_, antenna) <- antennas.toSet
      coords = antenna.coordinates
      i <- coords.indices
      j <- (i + 1) until coords.length
      (x1, y1) = coords(i)
      (x2, y2) = coords(j)
      dx = x2 - x1
      dy = y2 - y1
      d = if (dx != 0 && dy != 0) gcd(math.abs(dx), math.abs(dy)) else math.max(math.abs(dx), math.abs(dy))
      unitDx = dx / d
      unitDy = dy / d
      pos <- List((x1 - unitDx, y1 - unitDy), (x2 + unitDx, y2 + unitDy))
      if pos._1 >= 0 && pos._1 < rows && pos._2 >= 0 && pos._2 < cols
    } yield pos

    antinodes
  }

  def findAntinodesPart2(grid: Array[Array[Char]], antennas: Map[Char, Antenna]): Set[(Int, Int)] = {
    val rows = grid.length
    val cols = grid(0).length

    val antinodes = for {
      (_, antenna) <- antennas.toSet
      coords = antenna.coordinates
      if coords.length >= 2
      i <- coords.indices
      j <- (i + 1) until coords.length
      p1 = coords(i)
      p2 = coords(j)
      point <- findAllCollinearPoints(p1, p2, rows, cols)
    } yield point

    antinodes
  }

  def solvePart1(input: String): Int = {
    val (grid, antennas) = parseMap(input)
    findAntinodesPart1(grid, antennas).size
  }

  def solvePart2(input: String): Int = {
    val (grid, antennas) = parseMap(input)
    findAntinodesPart2(grid, antennas).size
  }


@main def day8(args: String*): Unit = {  // Changed Array[String] to String*
  // Test examples
  val example1 =
    """............
      |........0...
      |.....0......
      |.......0....
      |....0.......
      |......A.....
      |............
      |............
      |........A...
      |.........A..
      |............
      |............""".stripMargin

  val exampleT =
    """T.........
      |...T......
      |.T........
      |..........
      |..........
      |..........
      |..........
      |..........
      |..........
      |..........""".stripMargin

  // Run tests
  val part1Result = Day8.solvePart1(example1)
  println(s"Part 1 example result: $part1Result")
  assert(part1Result == 14, s"Expected 14, got $part1Result")

  val tResult = Day8.solvePart2(exampleT)
  println(s"Part 2 T example result: $tResult")
  assert(tResult == 9, s"Expected 9, got $tResult")

  val part2Result = Day8.solvePart2(example1)
  println(s"Part 2 example result: $part2Result")
  assert(part2Result == 34, s"Expected 34, got $part2Result")

  // Process actual input if provided
  if (args.nonEmpty) {  // Changed length > 0 to nonEmpty for Seq
    val input = Day8.readInput(args(0))
    println(s"Part 1: ${Day8.solvePart1(input)}")
    println(s"Part 2: ${Day8.solvePart2(input)}")
  }
}