def MakeFile():
    file=r"""XRUN = xrun
VCS  = vcs
IV   = iverilog

all: clean iverilog

iverilog:
	iverilog -o test {} ram* utils.vh
	vvp test
	rm -f *.mif *.hex *.vvp test
	
xrun:
	xrun -gui -xprop F utils.vh {} ram* -access +rwc
	
clean:
	rm -f *.mif *.hex *.vvp *.vcd *.txt test

.PHONY: clean"""
    return file

def ram_dummy_1rw():
    file=r'''`include "utils.vh"
module ram_generic_1rw
 #(  parameter NUM_WMASKS    = {},
     parameter MEMD = {},
     parameter DATA_WIDTH    = {}, // data width
     parameter nRPORTS = 1 , // number of reading ports
     parameter nWPORTS = 1, // number of write ports
     parameter IZERO   = 0 , // binary / Initial RAM with zeros (has priority over IFILE)
     parameter IFILE   = "",  // initialization mif file (don't pass extension), optional
     parameter BASIC_MODEL = {},
     parameter ADDR_WIDTH = {},
     parameter BASIC_DATA_WIDTH = {},
     parameter fixed_width = {},
     parameter DELAY = 3,
     parameter BYPASS = 1
  )( `ifdef USE_POWER_PINS
  inout vccd1,
  inout vssd1,
`endif
  input  clk, // clock
  input  csb, // active low chip select
  input  web, // active low write control
  input [NUM_WMASKS-1:0]  wmask, // write mask
  input [ADDR_WIDTH-1:0]  addr,
  input [DATA_WIDTH-1:0]  din,
  output reg[DATA_WIDTH-1:0]  dout,
  input clk1,
  input csb1,
  input [ADDR_WIDTH-1:0] addr1,
  output reg [DATA_WIDTH-1:0] dout1);

localparam ADDRW = ADDR_WIDTH; // address width
localparam NUM_OF_BANKS = MEMD / BASIC_MODEL;
localparam Basic_ADDRW = `log2(BASIC_MODEL); // address width
localparam horizontal_banks = DATA_WIDTH / BASIC_DATA_WIDTH;

reg [DATA_WIDTH-1:0] RData_out;
wire[DATA_WIDTH-1:0] Rdata [NUM_OF_BANKS-1:0];
wire [$clog2(NUM_OF_BANKS):0] Addr_sel;
reg  [$clog2(NUM_OF_BANKS):0] Raddr_sel; 
reg [Basic_ADDRW-1:0] Addr [NUM_OF_BANKS-1:0];
reg wen [NUM_OF_BANKS-1:0];
reg csb_i [NUM_OF_BANKS-1:0];
reg web_reg;

// port  2
reg [DATA_WIDTH-1:0] RData_out_1;
wire[DATA_WIDTH-1:0] Rdata_1 [NUM_OF_BANKS-1:0];
wire [$clog2(NUM_OF_BANKS):0] Addr_sel_1;
reg  [$clog2(NUM_OF_BANKS):0] Raddr_sel_1;
reg [Basic_ADDRW-1:0] Addr_1 [NUM_OF_BANKS-1:0];
reg csb_i_1 [NUM_OF_BANKS-1:0];


assign Addr_sel = addr / BASIC_MODEL;//addr % NUM_OF_BANKS;
assign Addr_sel_1 = addr1 / BASIC_MODEL; 

always @(posedge clk) begin
Raddr_sel <= addr / BASIC_MODEL; // addr % NUM_OF_BANKS;
Raddr_sel_1 <= addr1 / BASIC_MODEL;
web_reg <= web;
end

integer i;
integer j;

 always @* begin
	for(i=0; i<NUM_OF_BANKS; i=i+1) begin
	Addr[i] = (Addr_sel == i) ? addr : 0;
        wen[i] = (Addr_sel == i) ? web : 1;
	csb_i[i] = (Addr_sel == i) ? csb : 1;
	end
end

always @* begin
	for(i=0; i<NUM_OF_BANKS; i=i+1) begin
        Addr_1[i] = (Addr_sel_1 == i) ? addr1 : 0;
        csb_i_1[i] = (Addr_sel_1 == i) ? csb1 : 1;
	end
end

genvar p,h;
generate
	for(p=0; p<NUM_OF_BANKS; p=p+1) begin
		if(fixed_width == 32'h00000001) begin
			for(h=0; h<horizontal_banks; h=h+1) begin
			
			{} 
				ram_i ( `ifdef USE_POWER_PINS
					.vccd1(vccd1),
					.vssd1(vssd1),
					`endif
					.clk0(clk),
					.csb0(csb_i[p]),
					.web0(wen[p]),
					.wmask0(wmask[4*h +: 4]),
					.addr0(Addr[p]),
					.din0(din[BASIC_DATA_WIDTH*h +: BASIC_DATA_WIDTH]),
					.dout0(Rdata[p][BASIC_DATA_WIDTH*h +: BASIC_DATA_WIDTH]),
               		        .clk1(clk1),
               		        .csb1(csb_i_1[p]),
               		        .addr1(Addr_1[p]),
               		        .dout1(Rdata_1[p][BASIC_DATA_WIDTH*h +: BASIC_DATA_WIDTH]));
             		end
             	end
             	else begin
             		{} 
				ram_i ( `ifdef USE_POWER_PINS
					.vccd1(vccd1),
					.vssd1(vssd1),
					`endif
					.clk0(clk),
					.csb0(csb_i[p]),
					.web0(wen[p]),
					.wmask0(wmask),
					.addr0(Addr[p]),
					.din0(din),
					.dout0(Rdata[p]),
               		        .clk1(clk1),
               		        .csb1(csb_i_1[p]),
               		        .addr1(Addr_1[p]),
               		        .dout1(Rdata_1[p]));
               end
               	        
	end
endgenerate

always @(posedge clk) begin
        if(web_reg==1) begin
	for(j=0; j<NUM_OF_BANKS; j=j+1) begin
	 RData_out = (Raddr_sel == j) ? Rdata[j] : RData_out;
	end
        end
        else
         RData_out = RData_out;
        // Port 2
end
always @(posedge clk) begin 
        for(j=0; j<NUM_OF_BANKS; j=j+1) begin
        //RData_out_1 = (Raddr_sel_1 == q) ? Rdata_1[q] : RData_out_1;
	if(Raddr_sel_1 == j) 
        RData_out_1 = Rdata_1[j];
        else
        RData_out_1 = RData_out_1;	
	end
end

always @* begin
dout = RData_out;
end


always @* begin 
dout1 = RData_out_1;
end

endmodule


'''
    return file

def ram_dummy_1rw_tb():
    file=r"""`include "utils.vh"

// set default value for the following parameters, if not defined from command-line
// memory depth
`ifndef WMASK
`define WMASK   {}
`endif

`ifndef MEMD
`define MEMD   {}
`endif
// data width
`ifndef DATAW
`define DATAW   {}
`endif
// number of reading ports
`ifndef nWPORTS
`define nWPORTS 1
`endif
// number of writing ports
`ifndef nRPORTS
`define nRPORTS 1
`endif
// Simulation cycles count
`ifndef CYCC
`define CYCC 1000
`endif

`ifndef Basic_Model
`define Basic_Model {}
`endif

`ifndef ADDRW 
`define ADDRW {}
`endif


// WDW (Write-During-Write) protection
`ifndef WDW
`define WDW 0
`endif

// WAW (Write-After-Write) protection
`ifndef WAW
`define WAW 1
`endif

// RDW (Read-During-Write) protection
`ifndef RDW
`define RDW 1
`endif

// RAW (Read-After-Write) protection
`ifndef RAW
`define RAW 1
`endif



module ram_generic_1rw_tb;

  localparam MEMD    = `MEMD         ; // memory depth
  localparam DATAW   = `DATAW        ; // data width
  localparam nRPORTS = `nRPORTS      ; // number of reading ports
  localparam nWPORTS = `nWPORTS      ; // number of writing ports
  localparam CYCC    = `CYCC         ; // simulation cycles count
  localparam ADDRW  = `ADDRW; // address size
  localparam VERBOSE = 0             ; // verbose logging (1:yes; 0:no)
  localparam CYCT    = 10            ; // cycle      time
  localparam RSTT    = 5.2*CYCT      ; // reset      time
  localparam TERFAIL = 0             ; // terminate if fail?
  localparam TIMEOUT = 2*CYCT*CYCC   ; // simulation time
  localparam BASIC_MODEL = `Basic_Model;

  reg                      clk = 1'b1                    ; // global clock
  reg                      rst = 1'b1                    ; // global reset
  reg  [nWPORTS-1:0      ] WEnb                          ; // write enable for each writing port
  reg  [ADDRW*nWPORTS-1:0] WAddr_pck                     ; // write addresses - packed from nWPORTS write ports
  reg  [ADDRW-1:0        ] WAddr_upk        [nWPORTS-1:0]; // write addresses - unpacked 2D array 
  reg  [ADDRW*nRPORTS-1:0] RAddr_pck                     ; // read  addresses - packed from nRPORTS  read  ports
  reg  [ADDRW-1:0        ] RAddr_upk        [nRPORTS-1:0]; // read  addresses - unpacked 2D array 
  reg  [DATAW*nWPORTS-1:0] WData_pck                     ; // write data - packed from nWPORTS read ports
  reg  [DATAW-1:0        ] WData_upk        [nWPORTS-1:0]; // write data - unpacked 2D array 
  wire [DATAW*nRPORTS-1:0] RData_pck_sram             ; // read  data - packed from nRPORTS read ports
  reg  [DATAW-1:0        ] RData_upk_sram [nRPORTS-1:0]; // read  data - unpacked 2D array 
  reg  [DATAW*nRPORTS-1:0] RData_pck_golden             ; // read  data - packed from nRPORTS read ports
  reg  [DATAW-1:0        ] RData_upk_golden [nRPORTS-1:0]; // read  data - unpacked 2D array 
  reg  [`WMASK*nWPORTS-1:0] wmask_pck	    		  ; // wmask packed
  reg  [`WMASK-1:0        ] wmask_upk	     [nWPORTS-1:0]; // wmask unpacked
  integer i,j; // general indeces

 // generates random ram hex/mif initializing files
  task genInitFiles;
    input [31  :0] DEPTH  ; // memory depth
    input [31  :0] WIDTH  ; // memoty width
    input [255 :0] INITVAL; // initial vlaue (if not random)
    input          RAND   ; // random value?
    input [1:8*20] FILEN  ; // memory initializing file name
    reg   [255 :0] ramdata;
    integer addr,hex_fd,mif_fd;
    begin
      // open hex/mif file descriptors
      hex_fd = $fopen({{FILEN,".hex"}},"w");
      mif_fd = $fopen({{FILEN,".mif"}},"w");
      // write mif header
      $fwrite(mif_fd,"WIDTH         = %0d;\n",WIDTH);
      $fwrite(mif_fd,"DEPTH         = %0d;\n",DEPTH);
      $fwrite(mif_fd,"ADDRESS_RADIX = HEX;\n"     );
      $fwrite(mif_fd,"DATA_RADIX    = HEX;\n\n"   );
      $fwrite(mif_fd,"CONTENT BEGIN\n"            );
      // write random memory lines
      for(addr=0;addr<DEPTH;addr=addr+1) begin
        if (RAND) begin
          `GETRAND(ramdata,WIDTH); 
        end else ramdata = INITVAL;
        $fwrite(hex_fd,"%0h\n",ramdata);
        $fwrite(mif_fd,"  %0h :  %0h;\n",addr,ramdata);
      end
      // write mif tail
      $fwrite(mif_fd,"END;\n");
      // close hex/mif file descriptors
      $fclose(hex_fd);
      $fclose(mif_fd);
    end
  endtask
  
  
  initial begin
  $dumpfile("simulation.vcd");
  $dumpvars(0,ram_generic_1rw_tb);
  end


  integer rep_fd, ferr;
  initial begin
    // write header
    //rep_fd = $fopen("sim.txt","r"); // try to open report file for read
    //$ferror(rep_fd,ferr);       // detect error
    //$fclose(rep_fd);
    rep_fd = $fopen("sim.txt","w"); // open report file for append
    if (1) begin     // if file is new (can't open for read); write header
      $fwrite(rep_fd,"=======================Simulation Results======================\n");
      $fwrite(rep_fd,"===============================================================\n");
      $fwrite(rep_fd,"Golden   Golden           Actual      Actual          Result   \n");
      $fwrite(rep_fd,"Model    Model            Model       Model                    \n");
      $fwrite(rep_fd,"RAddr    RData            RAddr       RData                    \n");
      $fwrite(rep_fd,"===============================================================\n");
      $fclose(rep_fd);
    end
   // rep_fd = $fopen("sim.txt","a+");
    $write("Simulating  RAM:\n");
    $write("Write ports  : %0d\n"  ,nWPORTS  );
    $write("Read ports   : %0d\n"  ,nRPORTS  );
    $write("Data width   : %0d\n"  ,DATAW    );
    $write("RAM depth    : %0d\n"  ,MEMD     );
    $write("Address width: %0d\n"  ,ADDRW    );
    $write("Memory Size : %0d KB \n\n", (MEMD*DATAW)/8000);
    //$fclose(rep_fd);
    // generate random ram hex/mif initializing file
    genInitFiles(MEMD,DATAW   ,0,1,"init_ram");
    // finish simulation
    #(TIMEOUT) begin 
      $write("*** Simulation terminated due to timeout\n");
      $finish;
    end
  end   
// generate clock and reset
  always  #(CYCT/2) clk = ~clk; // toggle clock
  initial #(RSTT  ) rst = 1'b0; // lower reset
  // pack/unpack data and addresses
  `ARRINIT;
  always @* begin
    `ARR2D1D(nRPORTS,ADDRW,RAddr_upk        ,RAddr_pck        );
    `ARR2D1D(nWPORTS,`WMASK,wmask_upk        ,wmask_pck        );
    `ARR2D1D(nWPORTS,ADDRW,WAddr_upk        ,WAddr_pck        ); 
    `ARR1D2D(nWPORTS,DATAW,WData_pck        ,WData_upk        );
    `ARR1D2D(nRPORTS,DATAW,RData_pck_sram   ,RData_upk_sram   );
    `ARR1D2D(nRPORTS,DATAW,RData_pck_golden ,RData_upk_golden );
end

  // register write addresses
  reg  [ADDRW-1:0        ] WAddr_r_upk   [nWPORTS-1:0]; // previous (registerd) write addresses - unpacked 2D array 
  always @(negedge clk)
    //WAddr_r_pck <= WAddr_pck;
    for (i=0;i<nWPORTS;i=i+1) WAddr_r_upk[i] <= WAddr_upk[i];

  // generate random write data and random write/read addresses; on falling edge
  reg wdw_addr; // indicates same write addresses on same cycle (Write-During-Write)
  reg waw_addr; // indicates same write addresses on next cycle (Write-After-Write)
  reg rdw_addr; // indicates same read/write addresses on same cycle (Read-During-Write)
  reg raw_addr; // indicates same read address on next cycle (Read-After-Write)

always @(negedge clk) begin
   // generate random write addresses; different that current and previous write addresses
     for (i=0;i<nWPORTS;i=i+1) begin
      wdw_addr = 1; waw_addr = 1;
      while (wdw_addr || waw_addr) begin
        `GETRAND(WAddr_upk[i],ADDRW);
        `GETRAND(wmask_upk[i],      `WMASK); 
        wdw_addr = 0; waw_addr = 0;
        if (!`WDW) for (j=0;j<i      ;j=j+1) wdw_addr = wdw_addr || (WAddr_upk[i] == WAddr_upk[j]  );
        if (!`WAW) for (j=0;j<nWPORTS;j=j+1) waw_addr = waw_addr || (WAddr_upk[i] == WAddr_r_upk[j]);
      end
    end

 // generate random read addresses; different that current and previous write addresses
    for (i=0;i<nRPORTS;i=i+1) begin
      rdw_addr = 1; raw_addr = 1;
      while (rdw_addr || raw_addr) begin
        `GETRAND(RAddr_upk[i],ADDRW);
        rdw_addr = 0; raw_addr = 0;
        if (!`RDW) for (j=0;j<nWPORTS;j=j+1) rdw_addr = rdw_addr || (RAddr_upk[i] == WAddr_upk[j]  );
        if (!`RAW) for (j=0;j<nWPORTS;j=j+1) raw_addr = raw_addr || (RAddr_upk[i] == WAddr_r_upk[j]);
      end
    end
  // generate random write data and write enables
    `GETRAND(WData_pck,DATAW*nWPORTS);
    `GETRAND(WEnb     ,      nWPORTS); 
    
	if (rst) WEnb=1'b0; //else WEnb={{nWPORTS{{1'b1}}}};
  end

integer cycc=1; // cycles count
integer pass;
always @(negedge clk) begin
    if (!rst) begin
        #(CYCT/10) // a little after falling edge
        #(CYCT/2) // a little after rising edge
        pass = (RData_pck_golden===RData_pck_sram);
        //if (cycc==CYCC) begin
    	rep_fd = $fopen("sim.txt","a+");
        $fwrite(rep_fd,"%-10d %-15h %-10d %-15h %-10s \n",RAddr_pck,RData_pck_golden,RAddr_pck,RData_pck_sram,pass?"pass":"fail");
        $fclose(rep_fd);
        if (cycc==CYCC) begin
	$finish;
	end
        cycc=cycc+1;
    end
end

// Golden model of SRAM
integer q,r;
reg [DATAW-1:0] mem [0:MEMD-1];
initial begin
      //$readmemh("init_ram.hex", mem);
      for(q=0; q<MEMD; q=q+1) mem[q] ={{DATAW{{1'b0}}}};
end
always @(posedge clk)
  begin
    if(WEnb) begin
    	for(r=0; r<`WMASK; r=r+1) begin
    		if(wmask_pck[r])
        		mem[WAddr_pck][8*r +: 8] = WData_pck[8*r +: 8];
    	end
    end
   else
        RData_pck_golden <= #(10) mem[RAddr_pck];
  end

// Actual Model
ram_generic_1rw #( .NUM_WMASKS (`WMASK),
     		    .MEMD(MEMD),
     		    .DATA_WIDTH(DATAW), // data width
                    .nRPORTS(nRPORTS), // number of reading ports
     		    .nWPORTS(nWPORTS), // number of write ports
     		    .IZERO  (1), // binary / Initial RAM with zeros (has priority over IFILE)
    		    .IFILE(""),  // initialization mif file (don't pass extension), optional
     		    .BASIC_MODEL (BASIC_MODEL),
         	    .ADDR_WIDTH(`log2(MEMD)),
     		    .DELAY (3))
ram_1rw          (  `ifdef USE_POWER_PINS
		    .vccd1(vccd1),
		    .vssd1(vssd1),
		    `endif
		    .clk(clk), // clock
  		    .csb(1'b0), // active low chip select
  		    .web(~WEnb), // active low write control
  		    .wmask(wmask_pck), // write mask
		    .addr((WEnb==1'b1)?WAddr_pck:RAddr_pck),
  		    .din(WData_pck),
   		    .dout(RData_pck_sram),
                    .clk1(clk),
                    .csb1(1'b1),
                    .addr1({{ADDRW{{1'b0}}}}),
                    .dout1());
endmodule

"""
    return file

def ram_dummy_nr1w():
    file=r"""`include "utils.vh"
module ram_generic_nr1w
 #(  parameter NUM_WMASKS    = {},
     parameter MEMD = {},
     parameter DATA_WIDTH    = {}, // data width
     parameter nRPORTS = {} , // number of reading ports
     parameter nWPORTS = 1, // number of write ports
     parameter IZERO   = 0 , // binary / Initial RAM with zeros (has priority over IFILE)
     parameter IFILE   = "",  // initialization mif file (don't pass extension), optional
     parameter BASIC_MODEL = {},
     parameter ADDR_WIDTH = {},
     parameter DELAY = 3,
     parameter BYPASS = 1
  )( `ifdef USE_POWER_PINS
  vccd1,
  vssd1,
`endif
  addr, clk, csb, web, wmask, din, dout, addr1, csb1, clk1, dout1);
  `ifdef USE_POWER_PINS
  inout vccd1;
  inout vssd1;
  `endif
  input  clk; // clock
  input  csb; // active low chip select
  input  web; // active low write control
  input [NUM_WMASKS-1:0]  wmask; // write mask
  input [ADDR_WIDTH * nRPORTS-1:0] addr;
  input [DATA_WIDTH-1:0]  din;
  output reg [DATA_WIDTH*nRPORTS-1:0]  dout;
  input clk1;
  input csb1;
  input [ADDR_WIDTH * nRPORTS-1:0] addr1;
  output reg [DATA_WIDTH*nRPORTS-1:0]  dout1;
    // unpacked read addresses/data
  reg  [ADDR_WIDTH-1:0] RAddr_upk [nRPORTS-1:0]; // read addresses - unpacked 2D array 
  wire [DATA_WIDTH-1:0] RData_upk [nRPORTS-1:0]; // read data      - unpacked 2D array 
  reg  [ADDR_WIDTH-1:0] RAddr_upk_1 [nRPORTS-1:0]; // read addresses - unpacked 2D array 
  wire [DATA_WIDTH-1:0] RData_upk_1 [nRPORTS-1:0]; // read data      - unpacked 2D array 

  // unpack read addresses; pack read data
  `ARRINIT;
  always @* begin
    `ARR1D2D(nRPORTS,ADDR_WIDTH,addr,RAddr_upk);
    `ARR2D1D(nRPORTS,DATA_WIDTH,RData_upk,dout);
    `ARR1D2D(nRPORTS,ADDR_WIDTH,addr1,RAddr_upk_1);
    `ARR2D1D(nRPORTS,DATA_WIDTH,RData_upk_1,dout1);
  end
genvar rpi;
  generate
    for (rpi=0 ; rpi<nRPORTS; rpi=rpi+1) begin
    ram_generic_1rw #( .NUM_WMASKS (NUM_WMASKS),
     		    .MEMD(MEMD),
     		    .DATA_WIDTH(DATA_WIDTH), // data width
                    .nRPORTS(1), // number of reading ports
      		    .nWPORTS(1), // number of write ports
     		    .IZERO  (IZERO), // binary / Initial RAM with zeros (has priority over IFILE)
    		    .IFILE   (IFILE),  // initialization mif file (don't pass extension), optional
     		    .BASIC_MODEL (BASIC_MODEL),
         	    .ADDR_WIDTH(ADDR_WIDTH),
     		    .DELAY (DELAY),
     		    .BYPASS(BYPASS))
    ram_1rw      ( `ifdef USE_POWER_PINS
    		    .vccd1(vccd1),
    		    .vssd1(vssd1),
    		    `endif
    		    .clk(clk), // clock
  		    .csb(csb), // active low chip select
  		    .web(web), // active low write control
  		    .wmask(wmask), // write mask
  		    .addr(RAddr_upk[rpi]/*(web == 0) ? RAddr_upk[0] : RAddr_upk[rpi]*/),
  		    .din(din),
   		    .dout(RData_upk[rpi]),
                    .clk1(clk1),
                    .csb1(csb1), 
                    .addr1(RAddr_upk_1[rpi]),
                    .dout1(RData_upk_1[rpi]));
    end
  endgenerate
endmodule

"""
    return file

def ram_dummy_nr1w_tb():
    file=r"""`include "utils.vh"

// set default value for the following parameters, if not defined from command-line
// memory depth
`ifndef WMASK
`define WMASK   {}
`endif

`ifndef MEMD
`define MEMD   {}
`endif
// data width
`ifndef DATAW
`define DATAW   {}
`endif
// number of reading ports
`ifndef nWPORTS
`define nWPORTS 1
`endif
// number of writing ports
`ifndef nRPORTS
`define nRPORTS {}
`endif
// Simulation cycles count
`ifndef CYCC
`define CYCC 1000
`endif

`ifndef Basic_Model
`define Basic_Model {}
`endif

`ifndef ADDRW 
`define ADDRW {}
`endif

// WDW (Write-During-Write) protection
`ifndef WDW
`define WDW 0
`endif

// WAW (Write-After-Write) protection
`ifndef WAW
`define WAW 1
`endif

// RDW (Read-During-Write) protection
`ifndef RDW
`define RDW 1
`endif

// RAW (Read-After-Write) protection
`ifndef RAW
`define RAW 1
`endif

module ram_generic_nr1w_tb;

  localparam MEMD    = `MEMD         ; // memory depth
  localparam DATAW   = `DATAW        ; // data width
  localparam nRPORTS = `nRPORTS      ; // number of reading ports
  localparam nWPORTS = `nWPORTS      ; // number of writing ports
  localparam CYCC    = `CYCC         ; // simulation cycles count
  
  localparam ADDRW  = `ADDRW; // address size
  localparam VERBOSE = 0             ; // verbose logging (1:yes; 0:no)
  localparam CYCT    = 10            ; // cycle      time
  localparam RSTT    = 5.2*CYCT      ; // reset      time
  localparam TERFAIL = 0             ; // terminate if fail?
  localparam TIMEOUT = 2*CYCT*CYCC   ; // simulation time
  localparam BASIC_MODEL = `Basic_Model;
  reg                      clk = 1'b0                    ; // global clock
  reg                      rst = 1'b1                    ; // global reset
  reg  [nWPORTS-1:0      ] WEnb                          ; // write enable for each writing port
  reg  [ADDRW*nWPORTS-1:0] WAddr_pck                     ; // write addresses - packed from nWPORTS write ports
  reg  [ADDRW-1:0        ] WAddr_upk        [nWPORTS-1:0]; // write addresses - unpacked 2D array 
  reg  [ADDRW*nRPORTS-1:0] RAddr_pck                     ; // read  addresses - packed from nRPORTS  read  ports
  reg  [ADDRW-1:0        ] RAddr_upk        [nRPORTS-1:0]; // read  addresses - unpacked 2D array 
  reg  [DATAW*nWPORTS-1:0] WData_pck                     ; // write data - packed from nWPORTS read ports
  reg  [DATAW-1:0        ] WData_upk        [nWPORTS-1:0]; // write data - unpacked 2D array 
  wire [DATAW*nRPORTS-1:0] RData_pck_sram             ; // read  data - packed from nRPORTS read ports
  reg  [DATAW-1:0        ] RData_upk_sram [nRPORTS-1:0]; // read  data - unpacked 2D array 
  reg [DATAW*nRPORTS-1:0] RData_pck_golden             ; // read  data - packed from nRPORTS read ports
  reg  [DATAW-1:0        ] RData_upk_golden [nRPORTS-1:0]; // read  data - unpacked 2D array 
  reg  [`WMASK*nWPORTS-1:0] wmask_pck	    		  ; // wmask packed
  reg  [`WMASK-1:0        ] wmask_upk	     [nWPORTS-1:0]; // wmask unpacked
  integer i,j; // general indeces

 // generates random ram hex/mif initializing files
  task genInitFiles;
    input [31  :0] DEPTH  ; // memory depth
    input [31  :0] WIDTH  ; // memoty width
    input [255 :0] INITVAL; // initial vlaue (if not random)
    input          RAND   ; // random value?
    input [1:8*20] FILEN  ; // memory initializing file name
    reg   [255 :0] ramdata;
    integer addr,hex_fd,mif_fd;
    begin
      // open hex/mif file descriptors
      hex_fd = $fopen({{FILEN,".hex"}},"w");
      mif_fd = $fopen({{FILEN,".mif"}},"w");
      // write mif header
      $fwrite(mif_fd,"WIDTH         = %0d;\n",WIDTH);
      $fwrite(mif_fd,"DEPTH         = %0d;\n",DEPTH);
      $fwrite(mif_fd,"ADDRESS_RADIX = HEX;\n"     );
      $fwrite(mif_fd,"DATA_RADIX    = HEX;\n\n"   );
      $fwrite(mif_fd,"CONTENT BEGIN\n"            );
      // write random memory lines
      for(addr=0;addr<DEPTH;addr=addr+1) begin
        if (RAND) begin
          `GETRAND(ramdata,WIDTH); 
        end else ramdata = INITVAL;
        $fwrite(hex_fd,"%0h\n",ramdata);
        $fwrite(mif_fd,"  %0h :  %0h;\n",addr,ramdata);
      end
      // write mif tail
      $fwrite(mif_fd,"END;\n");
      // close hex/mif file descriptors
      $fclose(hex_fd);
      $fclose(mif_fd);
    end
  endtask
  
   
  initial begin
  	$dumpfile("srimulation.vcd");
  	$dumpvars(0,ram_generic_nr1w_tb);
  end

  integer rep_fd, ferr;
  initial begin
    // write header
    //rep_fd = $fopen("sim.txt","r"); // try to open report file for read
    //$ferror(rep_fd,ferr);       // detect error
    //$fclose(rep_fd);
    rep_fd = $fopen("sim.txt","w"); // open report file for append
    if (1) begin     // if file is new (can't open for read); write header
      $fwrite(rep_fd,"===============================Simulation Results======================================\n");
      $fwrite(rep_fd,"=======================================================================================\n");
      $fwrite(rep_fd,"Golden   Golden     Golden          Actual       Actual     Actual          Result   \n");
      $fwrite(rep_fd,"Read     Model      Model           Read         Model      Model                    \n");
      $fwrite(rep_fd,"Port     RAddr      RData           Port         RAddr      RData                    \n");
      $fwrite(rep_fd,"=======================================================================================\n");
      $fclose(rep_fd);
    end
    $write("Simulating  RAM:\n");
    $write("Write ports  : %0d\n"  ,nWPORTS  );
    $write("Read ports   : %0d\n"  ,nRPORTS  );
    $write("Data width   : %0d\n"  ,DATAW    );
    $write("RAM depth    : %0d\n"  ,MEMD     );
    $write("Address width: %0d\n",ADDRW    );
    $write("Memory Size : %0d KB \n\n", (MEMD*DATAW)/8000);
    // generate random ram hex/mif initializing file
    genInitFiles(MEMD,DATAW   ,0,1,"init_ram");
    // finish simulation
    #(TIMEOUT) begin 
      $write("*** Simulation terminated due to timeout\n");
      $finish;
    end
  end

// generate clock and reset
  always  #(CYCT/2) clk = ~clk; // toggle clock
  initial #(RSTT  ) rst = 1'b0; // lower reset

  // pack/unpack data and addresses
  `ARRINIT;
  always @* begin
    `ARR2D1D(nRPORTS,ADDRW,RAddr_upk        ,RAddr_pck        );
    `ARR2D1D(nWPORTS,`WMASK,wmask_upk        ,wmask_pck        );
    `ARR2D1D(nWPORTS,ADDRW,WAddr_upk        ,WAddr_pck        );
    `ARR1D2D(nWPORTS,DATAW,WData_pck        ,WData_upk        );
    `ARR1D2D(nRPORTS,DATAW,RData_pck_sram   ,RData_upk_sram   );
    `ARR2D1D(nRPORTS,DATAW,RData_upk_golden ,RData_pck_golden );
end

  // register write addresses
  reg  [ADDRW-1:0        ] WAddr_r_upk   [nWPORTS-1:0]; // previous (registerd) write addresses - unpacked 2D array 
  always @(negedge clk)
    //WAddr_r_pck <= WAddr_pck;
    for (i=0;i<nWPORTS;i=i+1) WAddr_r_upk[i] <= WAddr_upk[i];

  // generate random write data and random write/read addresses; on falling edge
  reg wdw_addr; // indicates same write addresses on same cycle (Write-During-Write)
  reg waw_addr; // indicates same write addresses on next cycle (Write-After-Write)
  reg rdw_addr; // indicates same read/write addresses on same cycle (Read-During-Write)
  reg raw_addr; // indicates same read address on next cycle (Read-After-Write)

always @(negedge clk) begin
    // generate random write addresses; different that current and previous write addresses
     for (i=0;i<nWPORTS;i=i+1) begin
      wdw_addr = 1; waw_addr = 1;
      while (wdw_addr || waw_addr) begin
        `GETRAND(WAddr_upk[i],ADDRW);
        wdw_addr = 0; waw_addr = 0;
        if (!`WDW) for (j=0;j<i      ;j=j+1) wdw_addr = wdw_addr || (WAddr_upk[i] == WAddr_upk[j]  );
        if (!`WAW) for (j=0;j<nWPORTS;j=j+1) waw_addr = waw_addr || (WAddr_upk[i] == WAddr_r_upk[j]);
      end
    end

 // generate random read addresses; different that current and previous write addresses
    for (i=0;i<nRPORTS;i=i+1) begin
      rdw_addr = 1; raw_addr = 1;
      while (rdw_addr || raw_addr) begin
        `GETRAND(RAddr_upk[i],ADDRW);
        `GETRAND(wmask_upk[i],      `WMASK); 
        rdw_addr = 0; raw_addr = 0;
        if (!`RDW) for (j=0;j<nWPORTS;j=j+1) rdw_addr = rdw_addr || (RAddr_upk[i] == WAddr_upk[j]  );
        if (!`RAW) for (j=0;j<nWPORTS;j=j+1) raw_addr = raw_addr || (RAddr_upk[i] == WAddr_r_upk[j]);
      end
    end
  // generate random write data and write enables
    `GETRAND(WData_pck,DATAW*nWPORTS);
    `GETRAND(WEnb     ,      nWPORTS); 
	if (rst) WEnb=1'b0; //else WEnb={{nWPORTS{{1'b1}}}};
  end

integer cycc=1; // cycles count
integer pass;
integer p;
always @(negedge clk) begin
    if (!rst) begin
        #(CYCT/10) // a little after falling edge
        #(CYCT/2) // a little after rising edge
        
        //if (cycc==CYCC) begin
        for(p=0; p<nRPORTS; p=p+1) begin
            pass = (RData_upk_golden[p]===RData_upk_sram[p]);
    	    rep_fd = $fopen("sim.txt","a+");
            $fwrite(rep_fd,"%-10d %-10d %-15h %-10d %-10d %-15h %-10s \n",p,RAddr_upk[p],RData_upk_golden[p],p,RAddr_upk[p],RData_upk_sram[p],pass?"pass":"fail");
            $fclose(rep_fd);
        end
        if (cycc==CYCC) begin
	$finish;
	end
        cycc=cycc+1;
    end
end

// Golden model of SRAM
integer q,r,s;
reg [DATAW-1:0] mem [0:MEMD-1];
initial begin
//      $readmemh("init_ram.hex", mem);
        for(r=0; r<MEMD; r=r+1) mem[r] = {{DATAW{{1'b0}}}};
end
always @(posedge clk)
  begin
    if(WEnb) begin
    	for(s=0; s<`WMASK; s=s+1) begin
    		if(wmask_pck[s])
        		mem[WAddr_pck][8*s +: 8] = WData_pck[8*s +: 8];
    	end
    end
   else begin
      for(q=0; q<nRPORTS; q=q+1) begin
        RData_upk_golden[q] <= #(10) mem[RAddr_upk[q]];
      end
   end
  end


ram_generic_nr1w #( .NUM_WMASKS (`WMASK),
     		    .MEMD(MEMD),
     		    .DATA_WIDTH(DATAW), // data width
                    .nRPORTS(nRPORTS), // number of reading ports
     		    .nWPORTS(nWPORTS), // number of write ports
     		    .IZERO  (1), // binary / Initial RAM with zeros (has priority over IFILE)
    		    .IFILE   (""),  // initialization mif file (don't pass extension), optional
     		    .BASIC_MODEL (BASIC_MODEL),
         	    .ADDR_WIDTH(ADDRW),
     		    .DELAY (3))
ram_nr1w          ( `ifdef USE_POWER_PINS
		    .vccd1(vccd1),
		    .vssd1(vssd1),
		    `endif
		    .clk(clk), // clock
  		    .csb(1'b0), // active low chip select
  		    .web(~WEnb), // active low write control
  		    .wmask(wmask_pck), // write mask
		    .addr((WEnb==1'b1)? {{nRPORTS{{WAddr_pck}}}}:RAddr_pck),
  		    .din(WData_pck),
   		    .dout(RData_pck_sram),
                    .clk1(clk),
                    .csb1(1'b1),
                    .addr1({{ADDRW*nRPORTS{{1'b0}}}}),
                    .dout1());
endmodule

"""
    return file

def ram_dummy_nrnw():
    file= r"""`include "utils.vh"
module ram_generic_nrnw
 #(  parameter NUM_WMASKS    = {},
     parameter MEMD = {},
     parameter DATA_WIDTH    = {}, // data width
     parameter nRPORTS = {} , // number of reading ports
     parameter nWPORTS = {}, // number of write ports
     parameter IZERO   = 0 , // binary / Initial RAM with zeros (has priority over IFILE)
     parameter IFILE   = "",  // initialization mif file (don't pass extension), optional
     parameter BASIC_MODEL ={},
     parameter ADDR_WIDTH = {},
     parameter DELAY = 3,
     parameter BYPASS = "RAW"
  )( `ifdef USE_POWER_PINS
  	vccd1;
  	vssd1;
     `endif
  addrW, addrR, clk, csb, web, wmask, din, dout, clk1, csb1, addrR_1, dout1);
  `ifdef USE_POWER_PINS
  inout vccd1;
  inout vssd1;
  `endif
  input  clk; // clock
  input  csb; // active low chip select
  input [             nWPORTS-1:0] web; // active low write control
  input [NUM_WMASKS * nWPORTS-1:0] wmask; // write mask
  input [ADDR_WIDTH * nWPORTS-1:0] addrW;
  input [ADDR_WIDTH * nRPORTS-1:0] addrR;
  input [DATA_WIDTH * nWPORTS-1:0]  din;
  output reg [DATA_WIDTH*nRPORTS-1:0]  dout;
  input clk1;
  input csb1;
  input [ADDR_WIDTH * nRPORTS-1:0] addrR_1;
  output reg [DATA_WIDTH*nRPORTS-1:0]  dout1;

  reg [ADDR_WIDTH*nWPORTS-1:0] WAddr_r; // registered write addresses - packed from nWPORTS write ports
  reg [DATA_WIDTH*nWPORTS-1:0] WData_r; // registered write data - packed from nWPORTS read ports
  reg [      nWPORTS-1:0] WEnb_r ; // registered write enable for each writing port
  reg [NUM_WMASKS*nWPORTS-1:0] WMask_r;

  reg [ADDR_WIDTH*nWPORTS-1:0] WAddr_r_1; // registered write addresses - packed from nWPORTS write ports
  reg [DATA_WIDTH*nWPORTS-1:0] WData_r_1; // registered write data - packed from nWPORTS read ports
  reg [      nWPORTS-1:0] WEnb_r_1 ; // registered write enable for each writing port
  reg [NUM_WMASKS*nWPORTS-1:0] WMask_r_1;

  reg [ADDR_WIDTH*nWPORTS-1:0] WAddr_r_2; // registered write addresses - packed from nWPORTS write ports
  reg [      nWPORTS-1:0] WEnb_r_2 ; // registered write enable for each writing port

 always @(posedge clk) begin
    WAddr_r <= addrW;
    WData_r <= din;
    WEnb_r  <= web;
    WMask_r <= wmask;
  end
 always @(posedge clk) begin
    WAddr_r_1 <= WAddr_r;
    WData_r_1 <= WData_r;
    WEnb_r_1  <= WEnb_r;
    WMask_r_1 <= WMask_r;
  end

 always @(posedge clk) begin
    WAddr_r_2 <= WAddr_r_1;
    WEnb_r_2  <= WEnb_r_1;
  end

 // unpacked/pack addresses/data
  reg  [NUM_WMASKS            -1:0] WMask2D    [nWPORTS-1:0]             ; // write mask           / 2D
  reg  [NUM_WMASKS            -1:0] WMask2D_r  [nWPORTS-1:0]             ; // registered write mask / 2D
  reg  [ADDR_WIDTH            -1:0] WAddr2D    [nWPORTS-1:0]             ; // write addresses            / 2D
  reg  [ADDR_WIDTH            -1:0] WAddr2D_r  [nWPORTS-1:0]             ; // registered write addresses / 2D
  reg  [ADDR_WIDTH            -1:0] WAddr_upk_r  [nWPORTS-1:0]             ; // registered write addresses / 2D
  reg  [DATA_WIDTH            -1:0] WData2D    [nWPORTS-1:0]             ; // write data                 / 2D 
  reg  [DATA_WIDTH            -1:0] WData2D_r  [nWPORTS-1:0]             ; // registered write data      / 2D
  wire [DATA_WIDTH* nRPORTS   -1:0] RDataOut2D [nWPORTS-1:0]             ; // read data out              / 2D
  reg  [DATA_WIDTH            -1:0] RDataOut3D [nWPORTS-1:0][nRPORTS-1:0]; // read data out              / 3D
  reg  [ADDR_WIDTH*(nWPORTS-1)-1:0] RAddrFB2D  [nWPORTS-1:0]             ; // read address fb            / 2D
  reg  [ADDR_WIDTH            -1:0] RAddrFB3D  [nWPORTS-1:0][nWPORTS-2:0]; // read address fb            / 3D
  wire [DATA_WIDTH*(nWPORTS-1)-1:0] RDataFB2D  [nWPORTS-1:0]             ; // read data fb               / 2D
  reg  [DATA_WIDTH            -1:0] RDataFB3D  [nWPORTS-1:0][nWPORTS-2:0]; // read data fb               / 3D
  reg  [DATA_WIDTH            -1:0] WDataFB2D  [nWPORTS-1:0]             ; // write data                 / 2D
  reg  [DATA_WIDTH            -1:0] WDataFB2D_r[nWPORTS-1:0]             ; // write data                 / 2D
  reg  [DATA_WIDTH            -1:0] RData2D    [nRPORTS-1:0]             ; // read data                  / 2D  
  reg [DATA_WIDTH*nRPORTS-1:0]  RData1D;
  reg [DATA_WIDTH*nRPORTS-1:0]  RData1D_r;
  wire [DATA_WIDTH-1:0]  dummy;

  `ARRINIT;
  always @(*) begin
    `ARR1D2D(nWPORTS,          NUM_WMASKS,WMask_r   ,WMask2D   );
    `ARR1D2D(nWPORTS,          NUM_WMASKS,WMask_r_1 ,WMask2D_r );
    `ARR1D2D(nWPORTS,          ADDR_WIDTH,addrW     ,WAddr2D   );
    `ARR1D2D(nWPORTS,          ADDR_WIDTH,WAddr_r_2   ,WAddr_upk_r);
    `ARR1D2D(nWPORTS,          ADDR_WIDTH,WAddr_r_1 ,WAddr2D_r );
    `ARR1D2D(nWPORTS,          DATA_WIDTH,WData_r   ,WData2D   );
    `ARR1D2D(nWPORTS,          DATA_WIDTH,WData_r_1 ,WData2D_r );
    `ARR2D1D(nRPORTS,          DATA_WIDTH,RData2D   ,RData1D   );
    `ARR2D3D(nWPORTS,nRPORTS  ,DATA_WIDTH,RDataOut2D,RDataOut3D);
    `ARR3D2D(nWPORTS,nWPORTS-1,ADDR_WIDTH,RAddrFB3D ,RAddrFB2D );
    `ARR2D3D(nWPORTS,nWPORTS-1,DATA_WIDTH,RDataFB2D ,RDataFB3D );
  end

always @(negedge clk) if(WEnb_r_1!={{nWPORTS{{1'b0}}}}) RData1D_r = RData1D; else RData1D_r = RData1D_r;
always @(posedge clk) dout = RData1D_r;

 // Bypassing indicators
  localparam WAW =  BYPASS!="NON"               ; // allow Write-After-Write (need to bypass feedback ram)
  localparam RAW = (BYPASS=="RAW")||(BYPASS=="RDW"); // new data for Read-after-Write (need to bypass output ram)
  localparam RDW =  BYPASS=="RDW"               ; // new data for Read-During-Write

  genvar wpi;
  generate
    for (wpi=0 ; wpi<nWPORTS ; wpi=wpi+1) begin: RPORTwpi
 // feedback multiread ram instantiation
ram_generic_nr1w #( 	.NUM_WMASKS(NUM_WMASKS),
     		     	.MEMD(MEMD),
     			.DATA_WIDTH(DATA_WIDTH), // data width
     			.nRPORTS(nWPORTS-1), // number of reading ports
     			.nWPORTS(1), // number of write ports
    			.IZERO(IZERO),//(wpi>0)&&(IFILE!="")), // binary / Initial RAM with zeros (has priority over IFILE)
    			.IFILE(IFILE),  // initialization mif file (don't pass extension), optional
    			.BASIC_MODEL(BASIC_MODEL),
     			.ADDR_WIDTH(ADDR_WIDTH),
     			.DELAY(DELAY),
     			.BYPASS(WAW || RDW || RAW )
  		   )
	ram_fdb   ( `ifdef USE_POWER_PINS
  			.vccd1(vccd1),
  			.vssd1(vssd1),
`		    `endif
  			.addr({{nWPORTS-1{{WAddr2D_r[wpi]}}}}/*(WEnb_r[wpi] == 1'b0) ? {{nWPORTS-1{{WAddr2D_r[wpi]}}}} : RAddrFB2D[wpi]*/), 
			.clk(clk), 
			.csb(csb), 
			.web(WEnb_r_1[wpi]), 
			.wmask(WMask2D_r[wpi]),
			.din(WDataFB2D[wpi]),
			.dout(dummy),
                        .clk1(clk),
                        .csb1(csb),
                        .addr1(RAddrFB2D[wpi]),
                        .dout1(RDataFB2D[wpi]));
// output multiread ram instantiation
ram_generic_nr1w #( 	.NUM_WMASKS(NUM_WMASKS),
     		     	.MEMD(MEMD),
     			.DATA_WIDTH(DATA_WIDTH), // data width
     			.nRPORTS(nRPORTS), // number of reading ports
     			.nWPORTS(1), // number of write ports
    			.IZERO(IZERO),//(wpi>0)&&(IFILE!="")), // binary / Initial RAM with zeros (has priority over IFILE)
    			.IFILE(IFILE),  // initialization mif file (don't pass extension), optional
    			.BASIC_MODEL(BASIC_MODEL),
     			.ADDR_WIDTH(ADDR_WIDTH),
     			.DELAY(DELAY),
     			.BYPASS(RDW ? 2 : RAW       )
  		   )
	ram_nr1w   ( `ifdef USE_POWER_PINS
  			.vccd1(vccd1),
  			.vssd1(vssd1),
`		      `endif
  			.addr({{nRPORTS{{WAddr2D_r[wpi]}}}}/*(WEnb_r[wpi] == 1'b0) ? {{nRPORTS{{WAddr2D_r[wpi]}}}} : addrR*/), 
			.clk(clk), 
			.csb(csb), 
			.web(WEnb_r_1[wpi]), 
			.wmask(WMask2D_r[wpi]),
			.din(WDataFB2D[wpi]),
			.dout(dummy),
                        .clk1(clk),
                        .csb1(csb),
                        .addr1(addrR),
                        .dout1(RDataOut2D[wpi]));

    end
  endgenerate

  // combinatorial logic for output and feedback functions
  integer i,j,k;
  always @(*) begin
    // generate output read functions
    for(i=0;i<nRPORTS;i=i+1) begin
      RData2D[i] = RDataOut3D[0][i];
      for(j=1;j<nWPORTS;j=j+1) RData2D[i] = RData2D[i] ^ RDataOut3D[j][i];
    end
    // generate feedback functions    
    for(i=0;i<nWPORTS;i=i+1) WDataFB2D[i] = WData2D_r[i];
    for(i=0;i<nWPORTS;i=i+1) begin
      k = 0;
      for(j=0;j<nWPORTS-1;j=j+1) begin
        k=k+(j==i);
        RAddrFB3D[i][j] = WAddr2D[k];
        if(WAddr2D_r[k] == WAddr_upk_r[i] & WEnb_r_1[k] == WEnb_r_2[i])
        WDataFB2D[k] = WDataFB2D[k] ^ WDataFB2D_r[i];
        else
        WDataFB2D[k] = WDataFB2D[k] ^ RDataFB3D[i][j];
        k=k+1;
      end
    end

  end

integer m;
always @(posedge clk) begin
for(m=0; m<nWPORTS; m=m+1)
WDataFB2D_r[m] = WDataFB2D[m];
end

endmodule"""
    return file

def ram_dummy_nrnw_tb():
    file=r"""`include "utils.vh"

// set default value for the following parameters, if not defined from command-line
// memory depth
`ifndef WMASK
`define WMASK   {}
`endif

`ifndef MEMD
`define MEMD  {}
`endif
// data width
`ifndef DATAW
`define DATAW   {}
`endif
// number of reading ports
`ifndef nWPORTS
`define nWPORTS {}
`endif
// number of writing ports
`ifndef nRPORTS
`define nRPORTS {}
`endif
// Simulation cycles count
`ifndef CYCC
`define CYCC 1000
`endif

`ifndef Basic_Model
`define Basic_Model {}
`endif
 
 `ifndef ADDRW 
`define ADDRW {}
`endif

// WDW (Write-During-Write) protection
`ifndef WDW
`define WDW 0
`endif

// WAW (Write-After-Write) protection
`ifndef WAW
`define WAW 0
`endif

// RDW (Read-During-Write) protection
`ifndef RDW
`define RDW 0
`endif

// RAW (Read-After-Write) protection
`ifndef RAW
`define RAW 0
`endif
module ram_generic_nrnw_tb;

  localparam MEMD    = `MEMD         ; // memory depth
  localparam DATAW   = `DATAW        ; // data width
  localparam nRPORTS = `nRPORTS      ; // number of reading ports
  localparam nWPORTS = `nWPORTS      ; // number of writing ports
  localparam CYCC    = `CYCC         ; // simulation cycles count
  
  localparam ADDRW  = `ADDRW;// address size
  localparam VERBOSE = 0             ; // verbose logging (1:yes; 0:no)
  localparam CYCT    = 10            ; // cycle      time
  localparam RSTT    = 5.2*CYCT      ; // reset      time
  localparam TERFAIL = 0             ; // terminate if fail?
  localparam TIMEOUT = 2*CYCT*CYCC   ; // simulation time
  localparam BASIC_MODEL = `Basic_Model;

  reg                      clk = 1'b0                    ; // global clock
  reg                      rst = 1'b1                    ; // global reset
  reg  [nWPORTS-1:0      ] WEnb                          ; // write enable for each writing port
  reg  [nWPORTS-1:0      ] WEnb_r                          ; // write enable for each writing port
  reg  [nWPORTS-1:0      ] WEnb_r_1                          ; // write enable for each writing port
  reg  [ADDRW*nWPORTS-1:0] WAddr_pck                     ; // write addresses - packed from nWPORTS write ports
  reg  [ADDRW*nWPORTS-1:0] WAddr_pck_r                     ; // write addresses - packed from nWPORTS write ports
  reg  [ADDRW*nWPORTS-1:0] WAddr_pck_r_1                    ; // write addresses - packed from nWPORTS write ports
  reg  [ADDRW-1:0        ] WAddr_upk        [nWPORTS-1:0]; // write addresses - unpacked 2D array 
  reg  [ADDRW-1:0        ] WAddr_upk_r_1        [nWPORTS-1:0]; // write addresses - unpacked 2D array 
  reg  [ADDRW*nRPORTS-1:0] RAddr_pck                     ; // read  addresses - packed from nRPORTS  read  ports
  reg  [ADDRW-1:0        ] RAddr_upk        [nRPORTS-1:0]; // read  addresses - unpacked 2D array 
  reg  [DATAW*nWPORTS-1:0] WData_pck                     ; // write data - packed from nWPORTS read ports
  reg  [DATAW*nWPORTS-1:0] WData_pck_r                     ; // write data - packed from nWPORTS read ports
  reg  [DATAW*nWPORTS-1:0] WData_pck_r_1                     ; // write data - packed from nWPORTS read ports
  reg  [DATAW-1:0        ] WData_upk        [nWPORTS-1:0]; // write data - unpacked 2D array 
  reg  [DATAW-1:0        ] WData_upk_r_1        [nWPORTS-1:0]; // write data - unpacked 2D array 
  wire [DATAW*nRPORTS-1:0] RData_pck_sram             ; // read  data - packed from nRPORTS read ports
  reg  [DATAW-1:0        ] RData_upk_sram [nRPORTS-1:0]; // read  data - unpacked 2D array 
  reg [DATAW*nRPORTS-1:0] RData_pck_golden             ; // read  data - packed from nRPORTS read ports
  reg [DATAW*nRPORTS-1:0] RData_pck_golden_r             ; // read  data - packed from nRPORTS read ports
  reg [DATAW*nRPORTS-1:0] out             ; // read  data - packed from nRPORTS read ports
  reg  [DATAW-1:0        ] RData_upk_golden [nRPORTS-1:0]; // read  data - unpacked 2D array 
  reg  [DATAW-1:0        ] RData_upk_golden_r [nRPORTS-1:0]; // read  data - unpacked 2D array
  reg  [`WMASK*nWPORTS-1:0] wmask_pck	    		  ; // wmask packed
  reg  [`WMASK*nWPORTS-1:0] wmask_pck_r                  ; 
  reg  [`WMASK*nWPORTS-1:0] wmask_pck_r_1                ; 
  reg  [`WMASK-1:0        ] wmask_upk	     [nWPORTS-1:0]; // wmask unpacked
  reg  [`WMASK-1:0        ] wmask_upk_r_1   [nWPORTS-1:0];
  integer i,j; // general indeces

 // generates random ram hex/mif initializing files
  task genInitFiles;
    input [31  :0] DEPTH  ; // memory depth
    input [31  :0] WIDTH  ; // memoty width
    input [255 :0] INITVAL; // initial vlaue (if not random)
    input          RAND   ; // random value?
    input [1:8*20] FILEN  ; // memory initializing file name
    reg   [255 :0] ramdata;
    integer addr,hex_fd,mif_fd;
    begin
      // open hex/mif file descriptors
      hex_fd = $fopen({{FILEN,".hex"}},"w");
      mif_fd = $fopen({{FILEN,".mif"}},"w");
      // write mif header
      $fwrite(mif_fd,"WIDTH         = %0d;\n",WIDTH);
      $fwrite(mif_fd,"DEPTH         = %0d;\n",DEPTH);
      $fwrite(mif_fd,"ADDRESS_RADIX = HEX;\n"     );
      $fwrite(mif_fd,"DATA_RADIX    = HEX;\n\n"   );
      $fwrite(mif_fd,"CONTENT BEGIN\n"            );
      // write random memory lines
      for(addr=0;addr<DEPTH;addr=addr+1) begin
        if (RAND) begin
          `GETRAND(ramdata,WIDTH); 
        end else ramdata = INITVAL;
        $fwrite(hex_fd,"%0h\n",ramdata);
        $fwrite(mif_fd,"  %0h :  %0h;\n",addr,ramdata);
      end
      // write mif tail
      $fwrite(mif_fd,"END;\n");
      // close hex/mif file descriptors
      $fclose(hex_fd);
      $fclose(mif_fd);
    end
  endtask

  initial begin
   	$dumpfile("simulation.vcd");
   	$dumpvars(0,ram_generic_nrnw_tb);
   end
   
  integer rep_fd, ferr;
  initial begin
    // write header
    //rep_fd = $fopen("sim.txt","r"); // try to open report file for read
    //$ferror(rep_fd,ferr);       // detect error
    //$fclose(rep_fd);
    rep_fd = $fopen("sim.txt","w"); // open report file for append
    if (1) begin     // if file is new (can't open for read); write header
      $fwrite(rep_fd,"===============================Simulation Results======================================\n");
      $fwrite(rep_fd,"=======================================================================================\n");
      $fwrite(rep_fd,"Golden   Golden     Golden          Actual       Actual     Actual          Result   \n");
      $fwrite(rep_fd,"Read     Model      Model           Read         Model      Model                    \n");
      $fwrite(rep_fd,"Port     RAddr      RData           Port         RAddr      RData                    \n");
      $fwrite(rep_fd,"=======================================================================================\n");
      $fclose(rep_fd);
    end
    $write("Simulating  RAM:\n");
    $write("Write ports  : %0d\n"  ,nWPORTS  );
    $write("Read ports   : %0d\n"  ,nRPORTS  );
    $write("Data width   : %0d\n"  ,DATAW    );
    $write("RAM depth    : %0d\n"  ,MEMD     );
    $write("Address width: %0d\n",ADDRW    );
    $write("Memory Size : %0d KB \n\n", (MEMD*DATAW)/8000);
    // generate random ram hex/mif initializing file
    genInitFiles(MEMD,DATAW   ,0,1,"init_ram");
    // finish simulation
    #(TIMEOUT) begin 
      $write("*** Simulation terminated due to timeout\n");
      $finish;
    end
  end

// generate clock and reset
  always  #(CYCT/2) clk = ~clk; // toggle clock
  initial #(RSTT  ) rst = 1'b0; // lower reset

  // pack/unpack data and addresses
  `ARRINIT;
  always @* begin
    `ARR2D1D(nRPORTS,ADDRW,RAddr_upk        ,RAddr_pck        );
    `ARR2D1D(nWPORTS,`WMASK,wmask_upk       ,wmask_pck        );
    `ARR2D1D(nWPORTS,ADDRW,WAddr_upk        ,WAddr_pck        );
    `ARR1D2D(nWPORTS,DATAW,WData_pck        ,WData_upk        );
    `ARR1D2D(nWPORTS,`WMASK,wmask_pck_r_1        ,wmask_upk_r_1        );
    `ARR1D2D(nWPORTS,ADDRW,WAddr_pck_r_1        ,WAddr_upk_r_1        );
    `ARR1D2D(nWPORTS,DATAW,WData_pck_r_1        ,WData_upk_r_1        );
    `ARR1D2D(nRPORTS,DATAW,RData_pck_sram   ,RData_upk_sram   );
    `ARR2D1D(nRPORTS,DATAW,RData_upk_golden ,RData_pck_golden );
    `ARR1D2D(nRPORTS,DATAW,RData_pck_golden_r   ,RData_upk_golden_r   );
end

always @(posedge clk) if(WEnb_r_1!={{nWPORTS{{1'b1}}}}) RData_pck_golden_r = RData_pck_golden; else RData_pck_golden_r = RData_pck_golden_r;
//always @(posedge clk) if(WEnb_r_1=={{nWPORTS{{1'b1}}}}) out = RData_pck_golden_r; else out = RData_pck_golden;

  // register write addresses
  reg  [ADDRW-1:0        ] WAddr_r_upk   [nWPORTS-1:0]; // previous (registerd) write addresses - unpacked 2D array 
  reg  [ADDRW-1:0        ] WAddr_r1_upk   [nWPORTS-1:0]; // previous (registerd) write addresses - unpacked 2D array 
  always @(posedge clk) begin
    //WAddr_r_pck <= WAddr_pck;
    for (i=0;i<nWPORTS;i=i+1) WAddr_r_upk[i] <= WAddr_upk[i];
  end
  always @(negedge clk) begin
    for (i=0;i<nWPORTS;i=i+1) WAddr_r1_upk[i] <= WAddr_r_upk[i];
  end
  // generate random write data and random write/read addresses; on falling edge
  reg wdw_addr; // indicates same write addresses on same cycle (Write-During-Write)
  reg waw_addr; // indicates same write addresses on next cycle (Write-After-Write)
  reg rdw_addr; // indicates same read/write addresses on same cycle (Read-During-Write)
  reg raw_addr; // indicates same read address on next cycle (Read-After-Write)

always @(negedge clk) begin
    // generate random write addresses; different that current and previous write addresses
     for (i=0;i<nWPORTS;i=i+1) begin
      wdw_addr = 1; waw_addr = 1;
      while (wdw_addr || waw_addr) begin
        `GETRAND(WAddr_upk[i],ADDRW);
        `GETRAND(wmask_upk[i],`WMASK);
        wdw_addr = 0; waw_addr = 0;
        if (!`WDW) for (j=0;j<i      ;j=j+1) wdw_addr = wdw_addr || (WAddr_upk[i] == WAddr_upk[j]  || (WAddr_upk[i] == WAddr_r_upk[j]));
        if (!`WAW) for (j=0;j<nWPORTS;j=j+1) waw_addr = waw_addr || (WAddr_upk[i] == WAddr_r1_upk[j]) || (WAddr_upk[i] == WAddr_r_upk[j]);
      end
    end

 // generate random read addresses; different that current and previous write addresses
    for (i=0;i<nRPORTS;i=i+1) begin
      rdw_addr = 1; raw_addr = 1;
      while (rdw_addr || raw_addr) begin
        `GETRAND(RAddr_upk[i],ADDRW);
        rdw_addr = 0; raw_addr = 0;
        if (!`RDW) for (j=0;j<nWPORTS;j=j+1) rdw_addr = rdw_addr || (RAddr_upk[i] == WAddr_upk[j]  || (RAddr_upk[i] == WAddr_r_upk[j]));
        if (!`RAW) for (j=0;j<nWPORTS;j=j+1) raw_addr = raw_addr || (RAddr_upk[i] == WAddr_r1_upk[j]) || (RAddr_upk[i] == WAddr_r_upk[j]);
      end
    end
  // generate random write data and write enables
    `GETRAND(WData_pck,DATAW*nWPORTS);
    `GETRAND(WEnb     ,      nWPORTS); 
	if (rst) WEnb={{nWPORTS{{1'b0}}}}; //else WEnb={{nWPORTS{{1'b1}}}};
  end

integer cycc=1; // cycles count
integer pass;
integer p,o;
always @(negedge clk) begin
    if (!rst) begin
        #(CYCT/10) // a little after falling edge
        #(CYCT/2) // a little after rising edge
        
        //if (cycc==CYCC) begin
        for(p=0; p<nRPORTS; p=p+1) begin
            pass = (RData_upk_golden_r[p]===RData_upk_sram[p]);
    	    rep_fd = $fopen("sim.txt","a+");
            $fwrite(rep_fd,"%-10d %-10d %-15h %-10d %-10d %-15h %-10s \n",p,RAddr_upk[p],RData_upk_golden_r[p],p,RAddr_upk[p],RData_upk_sram[p],pass?"pass":"fail");
            $fclose(rep_fd);
        end
        
        if (cycc==CYCC) begin
	$finish;
	end
        cycc=cycc+1;
    end
end

// Golden model of SRAM
integer q;
integer r,s;
always @(posedge clk) begin
WEnb_r <= WEnb;
WAddr_pck_r <= WAddr_pck;
wmask_pck_r <= wmask_pck;
WData_pck_r <= WData_pck;
end

always @(posedge clk) begin
WEnb_r_1 <= WEnb_r;
WAddr_pck_r_1 <= WAddr_pck_r;
wmask_pck_r_1 <= wmask_pck_r;
WData_pck_r_1 <= WData_pck_r;
end

reg [DATAW-1:0] mem [0:MEMD-1];
initial begin
 for(i=0; i<MEMD; i=i+1) mem[i] = {{DATAW{{1'b0}}}};
end
always @(negedge clk)
  begin
   // if(WEnb) begin
    for(r=0; r<nWPORTS; r=r+1) begin
        if(WEnb_r_1[r]) begin
        	for(s=0; s<`WMASK; s=s+1) begin
    			if(wmask_upk_r_1[r][s])
        			mem[WAddr_upk_r_1[r]][8*s +: 8] = WData_upk_r_1[r][8*s +: 8];
        	end
        end
        end
end
always @(posedge clk) begin
   // for(r=0; r<nWPORTS; r=r+1) begin
           for(q=0; q<nRPORTS; q=q+1) begin
           //if(WEnb_r_1 != {{nWPORTS{{1'b1}}}})
           RData_upk_golden[q] <= #(10) mem[RAddr_upk[q]];
           end
  //  end
     end
     
  // Bypassing indicators
  localparam BYP = `RDW ? "RDW" : (`RAW ? "RAW" : (`WAW ? "WAW" : "NON"));
  
ram_generic_nrnw #( .NUM_WMASKS (`WMASK),
     		    .MEMD(MEMD),
     		    .DATA_WIDTH(DATAW), // data width
                    .nRPORTS(nRPORTS), // number of reading ports
     		    .nWPORTS(nWPORTS), // number of write ports
     		    .IZERO  (1), // binary / Initial RAM with zeros (has priority over IFILE)
    		    .IFILE   ("init_ram"),  // initialization mif file (don't pass extension), optional
     		    .BASIC_MODEL (BASIC_MODEL),
         	    .ADDR_WIDTH(ADDRW),
     		    .DELAY (3),
     		    .BYPASS(BYP))
ram_nrnw          ( `ifdef USE_POWER_PINS
		    .vccd1(vccd1),
		    .vssd1(vssd1),
		    `endif
		    .clk(clk), // clock
  		    .csb(1'b0), // active low chip select
  		    .web(~WEnb), // active low write control
  		    .wmask(wmask_pck), // write mask
                    .addrW(WAddr_pck),
		    .addrR(RAddr_pck),
  		    .din(WData_pck),
   		    .dout(RData_pck_sram),
                    .clk1(clk),
                    .csb1(1'b1),
                    .addrR_1({{ADDRW*nRPORTS{{1'b0}}}}),
                    .dout1()
);
endmodule"""
    return file

def sythtcl():
    file=r"""#!/usr/bin/tclsh

create_project synthesis ./ -part {} -force
add_files [glob ./*.v]
set_property top {} [current_fileset]
reset_run synth_1
launch_runs synth_1 -jobs 4
wait_on_run synth_1
reset_run impl_1
launch_runs impl_1 -jobs 4
wait_on_run impl_1
"""
    return file

def utilsvh():
    file= r"""////////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2013, University of British Columbia (UBC); All rights reserved. //
//                                                                                //
// Redistribution  and  use  in  source   and  binary  forms,   with  or  without //
// modification,  are permitted  provided that  the following conditions are met: //
//   * Redistributions   of  source   code  must  retain   the   above  copyright //
//     notice,  this   list   of   conditions   and   the  following  disclaimer. //
//   * Redistributions  in  binary  form  must  reproduce  the  above   copyright //
//     notice, this  list  of  conditions  and the  following  disclaimer in  the //
//     documentation and/or  other  materials  provided  with  the  distribution. //
//   * Neither the name of the University of British Columbia (UBC) nor the names //
//     of   its   contributors  may  be  used  to  endorse  or   promote products //
//     derived from  this  software without  specific  prior  written permission. //
//                                                                                //
// THIS  SOFTWARE IS  PROVIDED  BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" //
// AND  ANY EXPRESS  OR IMPLIED WARRANTIES,  INCLUDING,  BUT NOT LIMITED TO,  THE //
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE //
// DISCLAIMED.  IN NO  EVENT SHALL University of British Columbia (UBC) BE LIABLE //
// FOR ANY DIRECT,  INDIRECT,  INCIDENTAL,  SPECIAL,  EXEMPLARY, OR CONSEQUENTIAL //
// DAMAGES  (INCLUDING,  BUT NOT LIMITED TO,  PROCUREMENT OF  SUBSTITUTE GOODS OR //
// SERVICES;  LOSS OF USE,  DATA,  OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER //
// CAUSED AND ON ANY THEORY OF LIABILITY,  WHETHER IN CONTRACT, STRICT LIABILITY, //
// OR TORT  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE //
// OF  THIS SOFTWARE,  EVEN  IF  ADVISED  OF  THE  POSSIBILITY  OF  SUCH  DAMAGE. //
////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////
//                    utils.vh: Design utilities (pre-compile)                    //
//                                                                                //
//    Author: Ameer M. Abdelhadi (ameer@ece.ubc.ca, ameer.abdelhadi@gmail.com)    //
// SRAM-based Multi-ported RAMs; University of British Columbia (UBC), March 2013 //
////////////////////////////////////////////////////////////////////////////////////

`ifndef __UTILS_VH__
`define __UTILS_VH__

`define DEBUG_MODE // debug mode, comment this line for other modes
`define VERBOSE    // verbose debug, comment this line for other modes

// Initiate Array structure - use once before calling packing/unpacking modules
`define ARRINIT integer _i_,_j_
// pack/unpack 1D/2D/3D arrays; use in "always @*" if combinatorial
`define ARR2D1D(D1W,D2W,    SRC,DST) for(_i_=1;_i_<=(D1W);_i_=_i_+1)                                 DST[((D2W)*_i_-1)-:D2W] = SRC[_i_-1]
`define ARR1D2D(D1W,D2W,    SRC,DST) for(_i_=1;_i_<=(D1W);_i_=_i_+1)                                 DST[_i_-1] = SRC[((D2W)*_i_-1)-:D2W]
`define ARR2D3D(D1W,D2W,D3W,SRC,DST) for(_i_=0;_i_< (D1W);_i_=_i_+1) for(_j_=1;_j_<=(D2W);_j_=_j_+1) DST[_i_][_j_-1] = SRC[_i_][((D3W)*_j_-1)-:D3W]
`define ARR3D2D(D1W,D2W,D3W,SRC,DST) for(_i_=0;_i_< (D1W);_i_=_i_+1) for(_j_=1;_j_<=(D2W);_j_=_j_+1) DST[_i_][((D3W)*_j_-1)-:D3W] = SRC[_i_][_j_-1]

// print a 2-D array in a comma-delimited list
`define ARRPRN(ARRLEN,PRNSRC) for (_i_=(ARRLEN)-1;_i_>=0;_i_=_i_-1) $write("%c%h%c",(_i_==(ARRLEN)-1)?"[":"",PRNSRC[_i_],!_i_?"]":",")
// Initialize a vector with a specific width random number; extra bits are zero padded
`define GETRAND(RAND,RANDW) RAND=0; repeat ((RANDW)/32) RAND=(RAND<<32)|{$random}; RAND=(RAND<<((RANDW)%32))|({$random}>>(32-(RANDW)%32))

// factorial (n!)
`define fact(n)  ( ( ((n) >= 2      ) ? 2  : 1) * \
                   ( ((n) >= 3      ) ? 3  : 1) * \
                   ( ((n) >= 4      ) ? 4  : 1) * \
                   ( ((n) >= 5      ) ? 5  : 1) * \
                   ( ((n) >= 6      ) ? 6  : 1) * \
                   ( ((n) >= 7      ) ? 7  : 1) * \
                   ( ((n) >= 8      ) ? 8  : 1) * \
                   ( ((n) >= 9      ) ? 9  : 1) * \
                   ( ((n) >= 10     ) ? 10 : 1)   )

// ceiling of log2
`define log2(x)  ( ( ((x) >  1      ) ? 1  : 0) + \
                   ( ((x) >  2      ) ? 1  : 0) + \
                   ( ((x) >  4      ) ? 1  : 0) + \
                   ( ((x) >  8      ) ? 1  : 0) + \
                   ( ((x) >  16     ) ? 1  : 0) + \
                   ( ((x) >  32     ) ? 1  : 0) + \
                   ( ((x) >  64     ) ? 1  : 0) + \
                   ( ((x) >  128    ) ? 1  : 0) + \
                   ( ((x) >  256    ) ? 1  : 0) + \
                   ( ((x) >  512    ) ? 1  : 0) + \
                   ( ((x) >  1024   ) ? 1  : 0) + \
                   ( ((x) >  2048   ) ? 1  : 0) + \
                   ( ((x) >  4096   ) ? 1  : 0) + \
                   ( ((x) >  8192   ) ? 1  : 0) + \
                   ( ((x) >  16384  ) ? 1  : 0) + \
                   ( ((x) >  32768  ) ? 1  : 0) + \
                   ( ((x) >  65536  ) ? 1  : 0) + \
                   ( ((x) >  131072 ) ? 1  : 0) + \
                   ( ((x) >  262144 ) ? 1  : 0) + \
                   ( ((x) >  524288 ) ? 1  : 0) + \
                   ( ((x) >  1048576) ? 1  : 0) + \
                   ( ((x) >  2097152) ? 1  : 0) + \
                   ( ((x) >  4194304) ? 1  : 0)   )

// floor of log2
`define log2f(x) ( ( ((x) >= 2      ) ? 1  : 0) + \
                   ( ((x) >= 4      ) ? 1  : 0) + \
                   ( ((x) >= 8      ) ? 1  : 0) + \
                   ( ((x) >= 16     ) ? 1  : 0) + \
                   ( ((x) >= 32     ) ? 1  : 0) + \
                   ( ((x) >= 64     ) ? 1  : 0) + \
                   ( ((x) >= 128    ) ? 1  : 0) + \
                   ( ((x) >= 256    ) ? 1  : 0) + \
                   ( ((x) >= 512    ) ? 1  : 0) + \
                   ( ((x) >= 1024   ) ? 1  : 0) + \
                   ( ((x) >= 2048   ) ? 1  : 0) + \
                   ( ((x) >= 4096   ) ? 1  : 0) + \
                   ( ((x) >= 8192   ) ? 1  : 0) + \
                   ( ((x) >= 16384  ) ? 1  : 0) + \
                   ( ((x) >= 32768  ) ? 1  : 0) + \
                   ( ((x) >= 65536  ) ? 1  : 0) + \
                   ( ((x) >= 131072 ) ? 1  : 0) + \
                   ( ((x) >= 262144 ) ? 1  : 0) + \
                   ( ((x) >= 524288 ) ? 1  : 0) + \
                   ( ((x) >= 1048576) ? 1  : 0) + \
                   ( ((x) >= 2097152) ? 1  : 0) + \
                   ( ((x) >= 4194304) ? 1  : 0)   )

`endif //__UTILS_VH__"""
    return file