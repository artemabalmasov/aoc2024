import scala.collection.mutable
import scala.util.matching.Regex
import scala.annotation.tailrec
import scala.io.Source
import scala.util.{Try, Success, Failure}
import java.io.{File, PrintWriter}

object Day14p2 {
  case class Position(x: Int, y: Int) {
    def distanceTo(other: Position): Int =
      math.abs(x - other.x) + math.abs(y - other.y)
  }
  case class Velocity(x: Int, y: Int)
  case class Robot(initialPos: Position, velocity: Velocity)

  private val RobotPattern: Regex = """p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)""".r

  def parseRobot(line: String): Option[Robot] = line match {
    case RobotPattern(px, py, vx, vy) => Some(
      Robot(
        Position(px.toInt, py.toInt),
        Velocity(vx.toInt, vy.toInt)
      )
    )
    case _ => None
  }

  def getPositionAfterTime(pos: Int, vel: Int, size: Int, time: Int): Int = {
    val totalMovement = vel * time
    math.floorMod(pos + totalMovement, size)
  }

  def getRobotPositionAtTime(robot: Robot, width: Int, height: Int, time: Int): Position = {
    val x = getPositionAfterTime(robot.initialPos.x, robot.velocity.x, width, time)
    val y = getPositionAfterTime(robot.initialPos.y, robot.velocity.y, height, time)
    Position(x, y)
  }

  def hasEnoughClusteredRobots(positions: Seq[Position], minRobots: Int, maxDistance: Int): Boolean = {
//    ! positions.exists(pos =>
//      positions.count(other => pos != other && pos.distanceTo(other) <= maxDistance) < minRobots
//    )

      positions.count(pos =>
      positions.exists(other => pos != other && pos.distanceTo(other) <= maxDistance)
    ) > minRobots
  }

  def findConnectedGroup(
                          start: Position,
                          positions: Set[Position],
                          visited: Set[Position] = Set.empty
                        ): Set[Position] = {
    if (visited.contains(start) || !positions.contains(start)) {
      visited
    } else {
      val neighbors = Set(
        Position(start.y, start.x + 1),
        Position(start.y, start.x - 1),
        Position(start.y + 1, start.x),
        Position(start.y - 1, start.x)
      )

      val newVisited = visited + start
      neighbors.foldLeft(newVisited) { (accVisited, neighbor) =>
        findConnectedGroup(neighbor, positions, accVisited)
      }
    }
  }

  def hasConnectedCluster(positions: Seq[Position]): Boolean = {
    val posSet = positions.toSet
    positions.exists { startPos =>
      val group = findConnectedGroup(startPos, posSet)
      group.size >= 10
    }
  }

  def visualizePositions(positions: Seq[Position], width: Int, height: Int): String = {
    val grid = Array.fill(height)(Array.fill(width)('.'))
    positions.foreach { pos =>
      if (pos.x >= 0 && pos.x < width && pos.y >= 0 && pos.y < height) {
        grid(pos.y)(pos.x) = '#'
      }
    }
    grid.map(_.mkString).mkString("\n")
  }

  def isChristmasTreePattern(positions: Seq[Position], width: Int, height: Int): Boolean = {
    val rowsByY = positions.groupBy(_.y).view.mapValues(_.map(_.x).toSet)
    val yCoords = rowsByY.keys.toSeq.sorted

    if (yCoords.length < 5) return false

    var starFound = false
    var trunkFound = false
    var hasWideSection = false

    for (y <- yCoords) {
      val rowWidth = rowsByY(y).size

      if (rowWidth == 1) {
        if (!starFound) {
          starFound = true
        } else if (!trunkFound && hasWideSection) {
          trunkFound = true
        }
      } else if (rowWidth > 1) {
        if (!starFound) return false
        if (trunkFound) return false
        hasWideSection = true
      }
    }

    starFound && trunkFound && hasWideSection
  }

  def findChristmasTreeTime(
                             robots: Seq[Robot],
                             width: Int = 101,
                             height: Int = 103,
                             maxTime: Int = 100000000,
                             minClusteredRobots: Int = 500,
                             maxDistance: Int = 2
                           ): Option[Int] = {
    val writer = new PrintWriter(new File("robot_positions.txt"))
    try {
      @tailrec
      def search(time: Int): Option[Int] = {
        if (time >= maxTime) None
        else {
          val positions = robots.map(getRobotPositionAtTime(_, width, height, time))
          val clusteredCount = positions.count(pos =>
            positions.exists(other => pos != other && pos.distanceTo(other) <= maxDistance)
          )
          println(s"Time: $time (Clustered robots: $clusteredCount)")
          if (hasConnectedCluster(positions)) {

            writer.println(s"Time: $time (Clustered robots: $clusteredCount)")
            writer.println(visualizePositions(positions, width, height))
            writer.println("\n")
            println(s"Time: $time (Clustered robots: $clusteredCount)")
            println(visualizePositions(positions, width, height))
            println("\n")
          }

//          if (isChristmasTreePattern(positions, width, height)) Some(time)
//          else
          search(time + 1)
        }
      }

      search(0)
    } finally {
      writer.close()
    }
  }

  def main(args: Array[String]): Unit = {
    if (args.length < 1 || args.length > 3) {
      println("Usage: scala RobotSimulation input_file [min_clustered_robots] [max_distance]")
      sys.exit(1)
    }

    val minClusteredRobots = if (args.length > 1) args(1).toInt else 5
    val maxDistance = if (args.length > 2) args(2).toInt else 5

    try {
      val source = Source.fromFile(args(0))
      try {
        val robots = source.getLines()
          .filter(_.nonEmpty)
          .flatMap(parseRobot)
          .toSeq

        findChristmasTreeTime(
          robots,
          minClusteredRobots = minClusteredRobots,
          maxDistance = maxDistance
        ) match {
          case Some(time) =>
            println(s"\nChristmas tree pattern appears after $time seconds")
            println(s"Used minimum clustered robots: $minClusteredRobots")
            println(s"Used maximum distance: $maxDistance")
            println("Position visualizations have been written to robot_positions.txt")
          case None =>
            println("\nNo Christmas tree pattern found within time limit")
            println(s"Used minimum clustered robots: $minClusteredRobots")
            println(s"Used maximum distance: $maxDistance")
            println("Position visualizations have been written to robot_positions.txt")
        }
      } finally {
        source.close()
      }
    } catch {
      case e: Exception =>
        println(s"Error processing input: ${e.getMessage}")
        sys.exit(1)
    }
  }
}