import scala.io.Source

object Day2:
  def isSafeReport(levels: Seq[Int]): Boolean =
    if levels.length < 2 then true
    else
      val differences = levels.sliding(2).map(w => w(1) - w(0)).toSeq

      // Check if all differences are within 1-3 range (absolute value)
      val validDifferences = differences.forall(diff => (1 to 3).contains(diff.abs))

      // Check if all differences have the same sign (all increasing or all decreasing)
      val consistent = differences.forall(_ > 0) || differences.forall(_ < 0)

      validDifferences && consistent

  def isSafeWithDampener(levels: Seq[Int]): Boolean =
  // First check if it's safe without dampener
    if isSafeReport(levels) then true
    else
    // Try removing each level one at a time
      levels.indices.exists(i =>
        val dampenedLevels = levels.patch(i, Seq(), 1)
        isSafeReport(dampenedLevels)
      )

  def parseInput(input: String): Seq[Seq[Int]] =
    input.trim.split("\n")
      .map(_.trim)
      .filter(_.nonEmpty)
      .map(_.split("\\s+").map(_.toInt).toSeq)
      .toSeq

  def solvePart1(input: String): Int =
    parseInput(input).count(isSafeReport)

  def solvePart2(input: String): Int =
    parseInput(input).count(isSafeWithDampener)

  def readFile(filename: String): String =
    val source = Source.fromFile(filename)
    try source.mkString finally source.close()

@main def day2(filename: String): Unit =
  val input = Day2.readFile(filename)
  val part1Result = Day2.solvePart1(input)
  val part2Result = Day2.solvePart2(input)

  println(s"Part 1 Result: $part1Result")
  println(s"Part 2 Result: $part2Result")

  // Test with example input
  val exampleInput = """
                       |7 6 4 2 1
                       |1 2 7 8 9
                       |9 7 6 2 1
                       |1 3 2 4 5
                       |8 6 4 4 1
                       |1 3 6 7 9
    """.stripMargin

  val examplePart1 = Day2.solvePart1(exampleInput)
  val examplePart2 = Day2.solvePart2(exampleInput)

  println("\nExample results:")
  println(s"Part 1: $examplePart1 (should be 2)")
  println(s"Part 2: $examplePart2 (should be 4)")

  assert(examplePart1 == 2, s"Part 1 example failed: expected 2, got $examplePart1")
  assert(examplePart2 == 4, s"Part 2 example failed: expected 4, got $examplePart2")