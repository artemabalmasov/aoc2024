import scala.io.Source

object Day23 {
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

  def findTriples(graph: Map[String, Set[String]]): Set[Set[String]] = {
    val computers = graph.keySet

    (for {
      a <- computers
      neighborsOfA = graph(a)
      b <- neighborsOfA
      if b > a  // avoid duplicates
      commonNeighbors = neighborsOfA.intersect(graph(b))
      c <- commonNeighbors
      if c > b  // maintain ordering
    } yield Set(a, b, c)).toSet
  }

  def solve(input: String): Int = {
    val connections = parseConnections(input)
    val graph = buildGraph(connections)
    val triples = findTriples(graph)

    triples.count(triple => triple.exists(_.startsWith("t")))
  }

  def main(args: Array[String]): Unit = {
    val input = Source.fromFile(args(0)).mkString
    val result = solve(input)
    println(s"Number of triples containing 't' computer: $result")
  }
}