import scala.io.Source

object Day7:
  case class Equation(testValue: Long, numbers: Seq[Long])

  def evaluateExpression(nums: Seq[Long], operators: Seq[String]): Long =
    operators.zip(nums.tail).foldLeft(nums.head) { case (result, (op, num)) =>
      op match
        case "+" => result + num
        case "*" => result * num
        case "||" => result.toString.concat(num.toString).toLong
    }

  def canMakeTestValuePart1(equation: Equation): Boolean =
    val numOperators = equation.numbers.length - 1

    (0 until (1 << numOperators)).exists { i =>
      val operators = (0 until numOperators).map { j =>
        if ((i & (1 << j)) != 0) "*" else "+"
      }.toSeq

      try
        evaluateExpression(equation.numbers, operators) == equation.testValue
      catch
        case _: NumberFormatException | _: ArithmeticException => false
    }

  def canMakeTestValuePart2(equation: Equation): Boolean =
    val numOperators = equation.numbers.length - 1

    def generateOperators(i: Int): Seq[String] =
      var temp = i
      (0 until numOperators).map { _ =>
        val op = temp % 3 match
          case 0 => "+"
          case 1 => "*"
          case 2 => "||"
        temp = temp / 3
        op
      }

    (0 until math.pow(3, numOperators).toInt).exists { i =>
      try
        val operators = generateOperators(i)
        evaluateExpression(equation.numbers, operators) == equation.testValue
      catch
        case _: NumberFormatException | _: ArithmeticException => false
    }

  def parseInput(input: String): Seq[Equation] =
    input.trim.split("\n")
      .map(_.trim)
      .filter(_.nonEmpty)
      .map { line =>
        val Array(testPart, numsPart) = line.split(":")
        val testValue = testPart.trim.toLong
        val nums = numsPart.trim.split("\\s+").map(_.toLong).toSeq
        Equation(testValue, nums)
      }

  def solvePart1(input: String): Long =
    parseInput(input)
      .filter(canMakeTestValuePart1)
      .map(_.testValue)
      .sum

  def solvePart2(input: String): Long =
    parseInput(input)
      .filter(canMakeTestValuePart2)
      .map(_.testValue)
      .sum

  def readFile(filename: String): String =
    val source = Source.fromFile(filename)
    try source.mkString finally source.close()

@main def day7(filename: String): Unit =
  val input = Day7.readFile(filename)
  val part1Result = Day7.solvePart1(input)
  val part2Result = Day7.solvePart2(input)

  println(s"Part 1 Result: $part1Result")
  println(s"Part 2 Result: $part2Result")

  // Test with example input
  val exampleInput = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

  val examplePart1 = Day7.solvePart1(exampleInput)
  val examplePart2 = Day7.solvePart2(exampleInput)

  println("\nExample results:")
  println(s"Part 1: $examplePart1 (should be 3749)")
  println(s"Part 2: $examplePart2 (should be 11387)")

  assert(examplePart1 == 3749L, s"Part 1 example failed: expected 3749, got $examplePart1")
  assert(examplePart2 == 11387L, s"Part 2 example failed: expected 11387, got $examplePart2")