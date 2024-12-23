object Day17 {
  case class ProgramState(
                           registerA: Int,
                           registerB: Int,
                           registerC: Int,
                           instructionPointer: Int,
                           output: List[Int] = List.empty
                         )

  sealed trait Operand {
    def getValue(state: ProgramState): Int
  }

  case class LiteralOperand(value: Int) extends Operand {
    def getValue(state: ProgramState): Int = value
  }

  case class ComboOperand(value: Int) extends Operand {
    def getValue(state: ProgramState): Int = value match {
      case 0 | 1 | 2 | 3 => value
      case 4 => state.registerA
      case 5 => state.registerB
      case 6 => state.registerC
      case 7 => throw new IllegalArgumentException("Invalid combo operand 7")
    }
  }

  def executeInstruction(opcode: Int, operand: Int, state: ProgramState): ProgramState = {
    opcode match {
      case 0 => // adv - divide A by 2^operand
        val denominator = math.pow(2, ComboOperand(operand).getValue(state)).toInt
        state.copy(
          registerA = state.registerA / denominator,
          instructionPointer = state.instructionPointer + 2
        )

      case 1 => // bxl - XOR B with literal operand
        state.copy(
          registerB = state.registerB ^ LiteralOperand(operand).getValue(state),
          instructionPointer = state.instructionPointer + 2
        )

      case 2 => // bst - set B to operand mod 8
        state.copy(
          registerB = ComboOperand(operand).getValue(state) % 8,
          instructionPointer = state.instructionPointer + 2
        )

      case 3 => // jnz - jump if A is not zero
        if (state.registerA != 0) {
          state.copy(instructionPointer = LiteralOperand(operand).getValue(state))
        } else {
          state.copy(instructionPointer = state.instructionPointer + 2)
        }

      case 4 => // bxc - XOR B with C
        state.copy(
          registerB = state.registerB ^ state.registerC,
          instructionPointer = state.instructionPointer + 2
        )

      case 5 => // out - output operand mod 8
        val outputValue = ComboOperand(operand).getValue(state) % 8
        state.copy(
          output = state.output :+ outputValue,
          instructionPointer = state.instructionPointer + 2
        )

      case 6 => // bdv - divide A by 2^operand, store in B
        val denominator = math.pow(2, ComboOperand(operand).getValue(state)).toInt
        state.copy(
          registerB = state.registerA / denominator,
          instructionPointer = state.instructionPointer + 2
        )

      case 7 => // cdv - divide A by 2^operand, store in C
        val denominator = math.pow(2, ComboOperand(operand).getValue(state)).toInt
        state.copy(
          registerC = state.registerA / denominator,
          instructionPointer = state.instructionPointer + 2
        )
    }
  }

  def runProgram(program: Seq[Int], initialState: ProgramState): String = {
    def loop(state: ProgramState): ProgramState = {
      if (state.instructionPointer >= program.length) {
        state
      } else {
        val opcode = program(state.instructionPointer)
        val operand = program(state.instructionPointer + 1)
        loop(executeInstruction(opcode, operand, state))
      }
    }

    val finalState = loop(initialState)
    finalState.output.mkString(",")
  }

  def main(args: Array[String]): Unit = {
    // Example usage:
    val program = Seq(0, 1, 5, 4, 3, 0)
    val initialState = ProgramState(
      registerA = 729,
      registerB = 0,
      registerC = 0,
      instructionPointer = 0
    )

    val output = runProgram(program, initialState)
    println(s"Program output: $output")
  }
}