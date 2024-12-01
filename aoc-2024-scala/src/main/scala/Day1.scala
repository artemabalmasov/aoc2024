import scala.io.Source

object Day1:
  def calculateTotalDistance(left: Seq[Int], right: Seq[Int]): Int =
    val sortedLeft = left.sorted
    val sortedRight = right.sorted

    sortedLeft.zip(sortedRight)
      .map((l, r) => Math.abs(l - r))
      .sum

  def calculateSimilarityScore(left: Seq[Int], right: Seq[Int]): Int =
    // Count occurrences in right list
    val rightCounts = right.groupBy(identity).view.mapValues(_.size).toMap

    // For each number in left list, multiply by its count in right list
    left.map(num => num * rightCounts.getOrElse(num, 0)).sum

  def parseInput(input: String): (Seq[Int], Seq[Int]) =
    val pairs = input.trim.split("\n").map { line =>
      val numbers = line.trim.split("\\s+").map(_.toInt)
      (numbers(0), numbers(1))
    }

    val (left, right) = pairs.unzip
    (left.toSeq, right.toSeq)

  def solvePart1(input: String): Int =
    val (left, right) = parseInput(input)
    calculateTotalDistance(left, right)

  def solvePart2(input: String): Int =
    val (left, right) = parseInput(input)
    calculateSimilarityScore(left, right)

  def readFile(filename: String): String =
    val source = Source.fromFile(filename)
    try source.mkString finally source.close()

@main def day1(filename: String): Unit =
  val input = Day1.readFile(filename)
  val part1Result = Day1.solvePart1(input)
  val part2Result = Day1.solvePart2(input)

  println(s"Part 1 Result: $part1Result")
  println(s"Part 2 Result: $part2Result")