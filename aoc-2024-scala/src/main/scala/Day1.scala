object Day1:
  def calculateTotalDistance(left: Seq[Int], right: Seq[Int]): Int =
    val sortedLeft = left.sorted
    val sortedRight = right.sorted
    
    sortedLeft.zip(sortedRight)
      .map((l, r) => Math.abs(l - r))
      .sum

  def parseInput(input: String): (Seq[Int], Seq[Int]) =
    val pairs = input.trim.split("\n").map { line =>
      val numbers = line.trim.split("\\s+").map(_.toInt)
      (numbers(0), numbers(1))
    }
    
    val (left, right) = pairs.unzip
    (left.toSeq, right.toSeq)

  def solve(input: String): Int =
    val (left, right) = parseInput(input)
    calculateTotalDistance(left, right)

@main def day1(): Unit =
  val exampleInput = """
    |3 4
    |4 3
    |2 5
    |1 3
    |3 9
    |3 3
    """.stripMargin

  val result = Day1.solve(exampleInput)
  println(s"Result: $result")
