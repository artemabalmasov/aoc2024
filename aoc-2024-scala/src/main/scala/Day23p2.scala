import scala.io.Source
import scala.collection.mutable

object Day23p2 {
  case class Connection(a: String, b: String)

  def parseConnections(input: String): Set[Connection] = {
    input.trim.split("\n").map { line =>
      val parts = line.trim.split("-")
      Connection(parts(0), parts(1))
    }.toSet
  }

  def buildGraph(connections: Set[Connection]): Map[String, Set[String]] = {
    connections.foldLeft(Map.empty[String, Set[String]]) { (graph, conn) =>
      graph
        .updatedWith(conn.a)(neighbors => Some(neighbors.getOrElse(Set.empty) + conn.b))
        .updatedWith(conn.b)(neighbors => Some(neighbors.getOrElse(Set.empty) + conn.a))
    }
  }

  class CliqueFinder(graph: Map[String, Set[String]]) {
    private val cliqueCache = mutable.Map[Set[String], Boolean]()
    private val maxCliqueCache = mutable.Map[Set[String], Set[String]]()

    def isClique(computers: Set[String]): Boolean = {
      cliqueCache.getOrElseUpdate(computers, {
        computers.forall { computer =>
          val neighbors = graph(computer)
          computers.forall(other => other == computer || neighbors.contains(other))
        }
      })
    }

    def findMaximumCliqueFrom(candidates: Set[String]): Set[String] = {
      if (candidates.isEmpty) return Set.empty

      maxCliqueCache.getOrElseUpdate(candidates, {
        if (isClique(candidates)) {
          candidates
        } else {
          // Try removing each vertex and recursively find the maximum clique
          candidates.map(v =>
            findMaximumCliqueFrom(candidates - v)
          ).maxBy(_.size)
        }
      })
    }

    def findMaximumCliqueOptimized(): Set[String] = {
      // Start with vertices that have highest degree as they're most likely to be in max clique
      val sortedByDegree = graph.toSeq.sortBy(-_._2.size).map(_._1)
      var bestClique = Set.empty[String]
      var remainingCandidates = sortedByDegree.toSet

      while (remainingCandidates.nonEmpty && bestClique.size < remainingCandidates.size) {
        val vertex = remainingCandidates.head
        val potentialClique = findMaximumCliqueFrom(
          remainingCandidates.filter(v => graph(vertex).contains(v) || v == vertex)
        )

        if (potentialClique.size > bestClique.size) {
          bestClique = potentialClique
        }

        remainingCandidates = remainingCandidates - vertex
      }

      bestClique
    }
  }

  def generatePassword(clique: Set[String]): String = {
    clique.toList.sorted.mkString(",")
  }

  def solve(input: String): String = {
    val connections = parseConnections(input)
    val graph = buildGraph(connections)
    val cliqueFinder = new CliqueFinder(graph)
    val largestClique = cliqueFinder.findMaximumCliqueOptimized()
    generatePassword(largestClique)
  }

  def main(args: Array[String]): Unit = {
    val input = Source.fromFile(args(0)).mkString
    val password = solve(input)
    println(s"LAN party password: $password")
  }
}