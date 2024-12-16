import scala.annotation.tailrec
import scala.io.Source

object Day15 {
  sealed trait Cell
  case object Wall extends Cell
  case object Empty extends Cell
  case object Box extends Cell
  case object Robot extends Cell

  case class Position(row: Int, col: Int) {
    def move(direction: Char): Position = direction match {
      case '^' => copy(row = row - 1)
      case 'v' => copy(row = row + 1)
      case '<' => copy(col = col - 1)
      case '>' => copy(col = col + 1)
    }

    // Calculate GPS coordinate from the edges (including walls)
    def gpsCoordinate: Int = {
      // Since we're counting from the top-left edge of the entire map (including walls),
      // we don't need to adjust the row/col values
      100 * (row) + col
    }
  }

  case class Warehouse(
                        grid: Vector[Vector[Cell]],
                        robotPos: Position,
                        boxPositions: Set[Position]
                      ) {
    def height: Int = grid.length
    def width: Int = grid.headOption.map(_.length).getOrElse(0)

    def isWall(pos: Position): Boolean =
      pos.row < 0 || pos.row >= height || pos.col < 0 || pos.col >= width ||
        grid(pos.row)(pos.col) == Wall

    def hasBox(pos: Position): Boolean = boxPositions.contains(pos)

    def debug(): Unit = {
      for (row <- 0 until height) {
        for (col <- 0 until width) {
          val pos = Position(row, col)
          val char = if (pos == robotPos) '@'
          else if (hasBox(pos)) 'O'
          else if (grid(row)(col) == Wall) '#'
          else '.'
          print(char)
        }
        println()
      }
      println(s"Robot at: ${robotPos.row},${robotPos.col}")
      println(s"Box positions: ${boxPositions.map(p => s"(${p.row},${p.col})").mkString(", ")}")
      println()
    }

    def moveRobotAndBox(robotPos: Position, direction: Char): Option[(Position, Option[Position])] = {
      val newRobotPos = robotPos.move(direction)

      if (isWall(newRobotPos)) {
        None
      } else if (!hasBox(newRobotPos)) {
        Some((newRobotPos, None))
      } else {
        val newBoxPos = newRobotPos.move(direction)
        if (isWall(newBoxPos) || hasBox(newBoxPos)) {
          None
        } else {
          Some((newRobotPos, Some(newBoxPos)))
        }
      }
    }

    def processMove(direction: Char): Option[Warehouse] = {
      moveRobotAndBox(robotPos, direction).map { case (newRobotPos, maybeNewBoxPos) =>
        val newBoxPositions = maybeNewBoxPos match {
          case Some(newBoxPos) =>
            boxPositions - newRobotPos + newBoxPos
          case None =>
            boxPositions
        }
        copy(robotPos = newRobotPos, boxPositions = newBoxPositions)
      }
    }

    def calculateGPSSum: Int = {
      val sum = boxPositions.map(_.gpsCoordinate).sum
      println(s"GPS coordinates: ${boxPositions.map(p => s"(${p.row},${p.col}=${p.gpsCoordinate})").mkString(", ")}")
      sum
    }
  }

  def parseWarehouse(input: String): Warehouse = {
    val lines = input.trim.split("\n")
    var robotPos: Position = null
    val boxPositions = scala.collection.mutable.Set[Position]()

    val grid = lines.zipWithIndex.map { case (line, row) =>
      line.zipWithIndex.map { case (char, col) =>
        char match {
          case '#' => Wall
          case 'O' =>
            boxPositions += Position(row, col)
            Empty
          case '@' =>
            robotPos = Position(row, col)
            Empty
          case _ => Empty
        }
      }.toVector
    }.toVector

    val warehouse = Warehouse(grid, robotPos, boxPositions.toSet)
    println("Initial state:")
    warehouse.debug()
    warehouse
  }

  def parseMoves(input: String): String = {
    input.filterNot(c => c == '\n' || c == ' ')
  }

  def simulateWarehouse(initial: Warehouse, moves: String): Warehouse = {
    @tailrec
    def simulate(current: Warehouse, remainingMoves: List[Char]): Warehouse = {
      remainingMoves match {
        case Nil => current
        case move :: rest =>
          val next = current.processMove(move).getOrElse(current)
          simulate(next, rest)
      }
    }

    simulate(initial, moves.toList)
  }

  def solve(input: String): Int = {
    val parts = input.split("\n\n")
    val warehouse = parseWarehouse(parts(0))
    val moves = parseMoves(parts(1))

    println(s"Processing ${moves.length} moves")

    val finalWarehouse = simulateWarehouse(warehouse, moves)
    println("\nFinal state:")
    finalWarehouse.debug()
    finalWarehouse.calculateGPSSum
  }

  def main(args: Array[String]): Unit = {
    val input = Source.fromFile(args(0)).mkString
    val result = solve(input)
    println(s"Sum of GPS coordinates: $result")
  }
}